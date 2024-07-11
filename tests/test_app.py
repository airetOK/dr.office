import pytest
import os
from flask_jwt_extended import create_access_token, set_access_cookies
from app import app
from flask import jsonify
from unittest.mock import patch, Mock
import repository.users_repository as ur
from flask import template_rendered
from contextlib import contextmanager

DB_PATH = 'tests/repository/test.db'


@pytest.fixture(scope='session', autouse=True)
def client():
    os.environ["DB_PATH"] = DB_PATH
    ur.__connect(DB_PATH)
    ur.add_user({'username': 'user', 'password': 'test'})
    app.config.update({
        "TESTING": True,
        "JWT_SECRET_KEY": "secret",
        "JWT_COOKIE_CSRF_PROTECT": True,
        "JWT_CSRF_CHECK_FORM": True,
        "JWT_SESSION_COOKIE": False
    })

    yield app.test_client()
    os.remove(DB_PATH)


@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


""" test function to set token in cookies """
@app.route("/cookie_login", methods=["GET"])
def cookie_login():
    resp = jsonify(login=True)
    access_token = create_access_token("user")
    set_access_cookies(resp, access_token)
    return resp


def test_get_login_page(client):
    response = client.get("/login")
    assert b"title_pic.jpg" in response.data


def test_get_missing_token(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.location == "/login"


def test_login_unauthorized(client):
    response = client.post("/login", data={
        "username": "undefined",
        "password": "undefined",
    })
    assert response.status_code == 401


@patch('repository.users_repository.is_user_exists', Mock(return_value=True))
def test_login(client):
    response = client.post("/login", data={
        "username": "user",
        "password": "test",
    })
    assert response.status_code == 302
    assert response.location == "/"


@patch('repository.users_repository.is_user_exists', Mock(return_value=False))
def test_login_user_not_exists(client):
    response = client.post("/login", data={
        "username": "user",
        "password": "test",
    })
    assert response.status_code == 401


def test_get_office_page(client):
    client.get("/cookie_login")
    response = client.get("/")
    assert response.status_code == 200


@patch('repository.patients_repository.add_patient', Mock())
def test_add_patient(client):
    resp = client.get("/cookie_login")
    response = client.post("/add", data={
        "fullName": "test_patient",
        "csrf_token": resp.headers.getlist('Set-Cookie')[1].replace('csrf_access_token=', '').split(';', 1)[0]
    })
    assert response.status_code == 302
    assert response.location == "/"


@patch('repository.patients_repository.get_patient', Mock())
def test_get_update_patient_page(client):
    client.get("/cookie_login")
    response = client.get("/update/id")
    assert response.status_code == 200


@patch('repository.patients_repository.update_patient', Mock())
def test_update_patient(client):
    resp = client.get("/cookie_login")
    response = client.post("/update/id", data={
        "fullName": "test_patient",
        "csrf_token": resp.headers.getlist('Set-Cookie')[1].replace('csrf_access_token=', '').split(';', 1)[0]
    })
    assert response.status_code == 302
    assert response.location == "/"


@patch('repository.patients_repository.delete_patient', Mock())
def test_delete_patient(client):
    client.get("/cookie_login")
    response = client.get("/delete/id")
    assert response.status_code == 302
    assert response.location == "/"


def test_search_patients_by_full_name(client):
    client.get("/cookie_login")
    response = client.get("/search")
    assert response.status_code == 200


def test_get_page(client):
    client.get("/cookie_login")
    response = client.get("/page/1")
    assert response.status_code == 200


def test_get_search_page(client):
    client.get("/cookie_login")
    response = client.get("/search/page/1?fullName=test")
    assert response.status_code == 200


def test_register(client):
    response = client.post("/register", data={
        "username": "test",
        "password": "Qwerty1!"
    })
    assert response.status_code == 302


def test_register_user_already_exists(client):
    response = client.post("/register", data={
        "username": "test",
        "password": "Qwerty1!"
    })
    assert response.status_code == 401


def test_register_password_not_too_long(client):
    with captured_templates(app) as templates:
        response = client.post("/register", data={
            "username": "test_user",
            "password": "invalid"
        })
    assert response.status_code == 200
    assert len(templates) == 1
    template, context = templates[0]
    assert template.name == "login.html"
    assert context['message'] == """Пароль має бути не менше за 8
                літер та довше ніж 20 літер"""


def test_register_password_dont_have_symbol(client):
    with captured_templates(app) as templates:
        response = client.post("/register", data={
            "username": "testUser",
            "password": "Invalid12"
        })
    assert response.status_code == 200
    assert len(templates) == 1
    template, context = templates[0]
    assert template.name == "login.html"
    assert context['message'] == """Пароль має містити принаймні одну велику англійську літеру,
                                        принаймні одну малу англійську літеру,
                                        принаймні одну цифру,
                                        принаймні один символ"""


def test_register_username_has_unexpected_symbol(client):
    with captured_templates(app) as templates:
        response = client.post("/register", data={
            "username": "test_user",
            "password": "Invalid12"
        })
    assert response.status_code == 200
    assert len(templates) == 1
    template, context = templates[0]
    assert template.name == "login.html"
    assert context['message'] == """Юзернейм має складатись з
                латинських літер або цифр"""


def test_register_username_is_too_long(client):
    with captured_templates(app) as templates:
        response = client.post("/register", data={
            "username": "loooooooooooongnaaaaame",
            "password": "Qwerty!1"
        })
    assert response.status_code == 200
    assert len(templates) == 1
    template, context = templates[0]
    assert template.name == "login.html"
    assert context['message'] == """Юзернейм має бути
                не довше 20 літер"""


def test_login_user_not_exists_template(client):
    with captured_templates(app) as templates:
        response = client.post("/login", data={
            "username": "notExists",
            "password": "test",
        })
    assert response.status_code == 401
    assert len(templates) == 1
    template, context = templates[0]
    assert template.name == "login.html"
    assert context['message'] == "Користувача не знайдено"


def test_forget_password_user_not_exists_template(client):
    with captured_templates(app) as templates:
        response = client.post("/forget-password", data={
            "username": "notExists",
            "password": "test",
        })
    assert response.status_code == 200
    assert len(templates) == 1
    template, context = templates[0]
    assert template.name == "login.html"
    assert context['forgetMessage'] == "Користувача з таким ім\'ям не існує"

def test_forget_password_password_incorrect(client):
    with captured_templates(app) as templates:
        response = client.post("/forget-password", data={
            "username": "user",
            "password": "test",
        })
    assert response.status_code == 200
    assert len(templates) == 1
    template, context = templates[0]
    assert template.name == "login.html"
    assert context['forgetMessage'] == """Пароль має бути не менше за 8
                літер та довше ніж 20 літер"""

@patch('repository.users_repository.set_password', Mock())
def test_forget_password_new_password(client):
    with captured_templates(app) as templates:
        response = client.post("/forget-password", data={
            "username": "user",
            "password": "Qwerty1!",
        })
    assert response.status_code == 302
    assert ur.set_password.assert_called_once
