from flask import Flask, render_template, redirect, request
import repository.patients_repository as pr
from initdb import init_db

app = Flask(__name__)

@app.route("/")
def office():
    return render_template('office.html', patients=pr.get_patients())


@app.route("/add", methods=['POST'])
def add_patient():
    pr.add_patient(request.form)
    return redirect('/')

init_db()
if __name__ == "__main__":
    app.run(debug=True)