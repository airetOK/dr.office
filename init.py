from flask import Flask, render_template, redirect, request
import repository.patients_repository as pr

app = Flask(__name__)

@app.route("/")
def office():
    return render_template('office.html', patients=pr.get_patients())


@app.route("/add", methods=['POST'])
def add_patient():
    pr.add_patient(request.form)
    return redirect('/')