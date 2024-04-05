from flask import Flask, render_template, redirect, request, make_response
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import os
import datetime
import math

import repository.patients_repository as pr
from util.language import get_language_names

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_CSRF_CHECK_FORM"] = True
app.config["JWT_SESSION_COOKIE"] = False
jwt = JWTManager(app)

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
    if username != os.getenv('JWT_USERNAME') or password != os.getenv('JWT_PASSWORD'):
        return make_response(render_template('login.html'), 401)
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=30))
    response = make_response(redirect('/'))
    set_access_cookies(response, access_token)
    return response

@app.route("/")
@jwt_required(locations=['cookies'])
def office():
    return render_template('office.html', 
                           patients=pr.get_patients(skip=0), 
                           languages=get_language_names(),
                           total_pages=math.ceil(float(pr.get_patients_count()/10)),
                           current_page=1)

@app.route("/page/<page>")
@jwt_required(locations=['cookies'])
def move_to_page(page):
    skip = int(page)*10 - 10
    return render_template('office.html', 
                           patients=pr.get_patients(skip=str(skip)), 
                           languages=get_language_names(),
                           total_pages=math.ceil(float(pr.get_patients_count()/10)),
                           current_page=int(page))


@app.route("/add", methods=['POST'])
@jwt_required(locations=['cookies'])
def add_patient():
    pr.add_patient(request.form)
    return redirect('/')

@app.route("/update/<id>", methods=['GET', 'POST'])
@jwt_required(locations=['cookies'])
def update_patient(id):
    if request.method == 'GET':
        return render_template('update-patient.html', patient=pr.get_patient(id), 
                               languages=get_language_names())
    pr.update_patient(request.form, id)
    return redirect('/')

@app.route("/delete/<id>")
@jwt_required(locations=['cookies'])
def delete_patient(id):
    pr.delete_patient(id)
    return redirect('/')

@app.route("/search")
@jwt_required(locations=['cookies'])
def search_patients_by_full_name():
    full_name = request.args.get("fullName")
    return render_template('search-office.html', patients=pr.get_patients_by_full_name(full_name, 0),
                           total_pages=math.ceil(float(pr.get_patients_by_full_name_count(full_name)/10)),
                           full_name=full_name,
                           current_page=1,
                           languages=get_language_names())

@app.route("/search/page/<page>")
@jwt_required(locations=['cookies'])
def move_to_search_page(page):
    full_name = request.args.get("fullName")
    skip = int(page)*10 - 10
    return render_template('search-office.html', 
                           patients=pr.get_patients_by_full_name(full_name, str(skip)), 
                           languages=get_language_names(),
                           total_pages=math.ceil(float(pr.get_patients_by_full_name_count(full_name)/10)),
                           full_name=full_name,
                           current_page=int(page))

if __name__ == "__main__":
    app.run(debug=True)