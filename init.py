from flask import Flask, render_template
from repository.patients_repository import get_patients

app = Flask(__name__)

@app.route("/")
def office():
    return render_template('office.html', patients=get_patients())