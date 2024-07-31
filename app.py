from flask import Flask, render_template, redirect, request, make_response
from flask_jwt_extended import (create_access_token, set_access_cookies, 
    jwt_required, get_jwt_identity, unset_jwt_cookies, JWTManager, get_jwt)
import os
import math
from datetime import datetime, timedelta, timezone
from functools import wraps

import repository.patients_repository as pr
import repository.users_repository as ur
from util.language import get_language_names
from util.users_validation import UsersValidation
from util.log_config import load_log_config
from dotenv import load_dotenv

'''Load env variables'''
load_dotenv()

'''Configure the Flask app and JWT token'''
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_CSRF_CHECK_FORM"] = True
app.config["JWT_SESSION_COOKIE"] = False
jwt = JWTManager(app)

'''Load custom logger'''
logger = load_log_config(__name__)

def request_log(func):
    @wraps(func)
    def inner(*args, **kwargs):
        logger.info(f"User: {get_jwt_identity()}, method: {request.method}, url: {request.url}")
        return func(*args, **kwargs)
    return inner

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(days=3))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(
                identity=get_jwt_identity(), expires_delta=timedelta(days=14))
            response = make_response(redirect('/'))
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@jwt.expired_token_loader
def expired_token_handler(arg1, arg2):
    ''' parameters should be present in functions's signature '''
    return redirect('/login')


@jwt.invalid_token_loader
def invalid_token_handler(arg):
    ''' parameters should be present in functions's signature '''
    return redirect('/login')


@jwt.unauthorized_loader
def missing_token_handler(arg):
    ''' parameters should be present in functions's signature '''
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form["username"]
    password = request.form["password"]
    if not ur.is_user_exists(username, password):
        return make_response(render_template('login.html', message='Користувача не знайдено'), 401)
    access_token = create_access_token(
        identity=username, expires_delta=timedelta(days=14))
    response = make_response(redirect('/'))
    set_access_cookies(response, access_token)
    return response


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    res = UsersValidation().are_username_and_password_valid(username, password)

    if not res.is_valid():
        return render_template('login.html', message=res.get_message())

    if ur.is_user_exists_with_username(username):
        return make_response(render_template('login.html', message='Користувач з таким ім\'ям існує'), 401)

    ur.add_user(request.form)

    access_token = create_access_token(
        identity=username, expires_delta=timedelta(days=14))
    response = make_response(redirect('/'))
    set_access_cookies(response, access_token)
    return response


@app.route("/")
@jwt_required(locations=['cookies'])
@request_log
def office():
    user_id = ur.get_id_by_username(get_jwt_identity())
    return render_template("office.html",
                           patients=pr.get_patients(user_id, skip=0),
                           languages=get_language_names(),
                           search_param="fullName",
                           total_pages=math.ceil(
                               float(pr.get_patients_count(user_id)/10)),
                           current_page=1)


@app.route("/logout", methods=["POST"])
def logout():
    resp = make_response(redirect('/login'))
    unset_jwt_cookies(resp)
    return resp


@app.route("/add", methods=['POST'])
@jwt_required(locations=['cookies'])
@request_log
def add_patient():
    user_id = ur.get_id_by_username(get_jwt_identity())
    pr.add_patient(request.form, user_id)
    return redirect('/')


@app.route("/update/<id>", methods=['GET', 'POST'])
@jwt_required(locations=['cookies'])
@request_log
def update_patient(id):
    user_id = ur.get_id_by_username(get_jwt_identity())
    if request.method == 'GET':
        return render_template('update-patient.html', patient=pr.get_patient(id, user_id),
                               languages=get_language_names())
    pr.update_patient(request.form, id, user_id)
    return redirect('/')


@app.route("/delete/<id>")
@jwt_required(locations=['cookies'])
@request_log
def delete_patient(id):
    user_id = ur.get_id_by_username(get_jwt_identity())
    pr.delete_patient(id, user_id)
    return redirect('/')


@app.route("/page/<page>")
@jwt_required(locations=['cookies'])
@request_log
def move_to_page(page):
    user_id = ur.get_id_by_username(get_jwt_identity())
    skip = int(page)*10 - 10
    return render_template('office.html',
                           patients=pr.get_patients(user_id, skip=str(skip)),
                           languages=get_language_names(),
                           search_param="fullName",
                           total_pages=math.ceil(
                               float(pr.get_patients_count(user_id)/10)),
                           current_page=int(page))


@app.route("/search/<param>")
@jwt_required(locations=['cookies'])
@request_log
def search_patients_by_full_name(param: str):
    user_id = ur.get_id_by_username(get_jwt_identity())
    value = request.args.get("searchValue")
    if param == "fullName":
        return render_template("search-office.html", patients=pr.get_patients_by_full_name(value, 0, user_id),
            total_pages=math.ceil(
            float(pr.get_patients_by_full_name_count(value, user_id)/10)),
            param="fullName",
            value=value,
            current_page=1,
            languages=get_language_names())
    elif param == "actions":
        return render_template("search-office.html", patients=pr.get_patients_by_actions(value, 0, user_id),
            total_pages=math.ceil(
            float(pr.get_patients_by_actions_count(value, user_id)/10)),
            param="actions",
            value=value,
            current_page=1,
            languages=get_language_names())


@app.route("/search/<param>/page/<page>")
@jwt_required(locations=['cookies'])
@request_log
def move_to_search_page(param, page):
    user_id = ur.get_id_by_username(get_jwt_identity())
    skip = int(page)*10 - 10
    if param == "fullName":
        full_name = request.args.get("fullName")
        return render_template('search-office.html',
            patients=pr.get_patients_by_full_name(
                full_name, str(skip), user_id),
            languages=get_language_names(),
            total_pages=math.ceil(
                float(pr.get_patients_by_full_name_count(full_name, user_id)/10)),
            param="fullName",
            value=full_name,
            current_page=int(page))
    elif param == "actions":
        actions = request.args.get("actions")
        return render_template('search-office.html',
            patients=pr.get_patients_by_actions(
                actions, str(skip), user_id),
            languages=get_language_names(),
            total_pages=math.ceil(
                float(pr.get_patients_by_actions_count(actions, user_id)/10)),
            param="actions",
            value=actions,
            current_page=int(page))

@app.route("/forget-password", methods=["POST"])
def forget_password():
    username = request.form["username"]
    password = request.form["password"]

    if not ur.is_user_exists_with_username(username):
        return render_template('login.html', forgetMessage="Користувача з таким ім\'ям не існує")

    res = UsersValidation().are_username_and_password_valid(username, password)
    if not res.is_valid():
        return render_template('login.html', forgetMessage=res.get_message())
    
    ur.set_password(username, password)
    access_token = create_access_token(
        identity=username, expires_delta=timedelta(days=14))
    response = make_response(redirect('/'))
    set_access_cookies(response, access_token)
    return response
