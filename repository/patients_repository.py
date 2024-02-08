from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
import sqlite3


def connect():
    try:
        with sqlite3.connect("patients.db") as conn:
            return conn
    except (Exception) as error:
        print(error)
    return conn

def add_patient(form: ImmutableMultiDict) -> None:
    conn = connect()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO patients(fullName, teeth, actions, price, date) VALUES ('{form['fullName']}', '{form['teeth']}', '{form['actions']}', '{form['price']}', '{__get_current_date()}')")
    conn.commit()
    cur.close()
    conn.close()

def get_patients() -> list[object]:
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT id, fullName, teeth, actions, price, date FROM patients')
    patients = __convert(cur.fetchall())
    cur.close()
    conn.close()
    print(patients)
    return patients

def __get_current_date() -> str:
    return datetime.today().strftime('%Y-%m-%d')

def __convert(db_list) -> list[object]:
    patients = []
    for id, fullName, teeth, actions, price, date in db_list:
        patients.append({'id': id,
                     'fullname': fullName,
                     'teeth': teeth,
                     'actions': actions,
                     'price': price,
                     'date': date})
    return patients