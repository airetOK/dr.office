from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
import sqlite3
import os


def __connect(path_to_db: str):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS patients(id INTEGER PRIMARY KEY, fullName NOT NULL, teeth, actions, price, date)')
            conn.commit()
            return conn
    except (Exception) as error:
        print(error)
    return conn

def add_patient(form: ImmutableMultiDict) -> None:
    conn = __connect(os.getenv('DB_PATH'))
    cur = conn.cursor()
    cur.execute(f"INSERT INTO patients(fullName, teeth, actions, price, date) VALUES ('{form['fullName']}', '{form['teeth']}', '{form['actions']}', '{form['price']}', '{__get_current_date()}')")
    conn.commit()
    cur.close()
    conn.close()

def get_patients() -> list[object]:
    conn = __connect(os.getenv('DB_PATH'))
    cur = conn.cursor()
    cur.execute('SELECT id, fullName, teeth, actions, price, date FROM patients')
    patients = __convert(cur.fetchall())
    cur.close()
    conn.close()
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