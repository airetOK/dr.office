import pytest
import os
from flask_jwt_extended import create_access_token, set_access_cookies
from app import app
from flask import jsonify
from unittest.mock import patch, Mock


@pytest.fixture()
def client():
    os.environ["JWT_USERNAME"] = "test_name"
    os.environ["JWT_PASSWORD"] = "test_pass"
    app.config.update({
        "TESTING": True,
        "JWT_SECRET_KEY": "secret",
        "JWT_COOKIE_CSRF_PROTECT": True,
        "JWT_CSRF_CHECK_FORM": True,
        "JWT_SESSION_COOKIE": False
    })

    yield app.test_client()

""" test function to set token in cookies """
@app.route("/cookie_login", methods=["GET"])
def cookie_login():
    resp = jsonify(login=True)
    access_token = create_access_token("test_name")
    set_access_cookies(resp, access_token)
    return resp

def test_get_login_page(client):
    response = client.get("/login")
    assert b"title_pic.jpg" in response.data

def test_login_unauthorized(client):
    response = client.post("/login", data={
        "username": "undefined",
        "password": "undefined",
    })
    assert response.status_code == 401

def test_login(client):
    response = client.post("/login", data={
        "username": "test_name",
        "password": "test_pass",
    })
    assert response.status_code == 302

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

@patch('repository.patients_repository.delete_patient', Mock())
def test_delete_patient(client):
    client.get("/cookie_login")
    response = client.get("/delete/id")
    assert response.status_code == 302

def test_search_patients_by_full_name(client):
    client.get("/cookie_login")
    response = client.get("/search")
    assert response.status_code == 200