from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
import sqlite3
import os


def __connect(path_to_db: str):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS patients(id INTEGER PRIMARY KEY, fullName NOT NULL, teeth, actions, price, comment, date)')
            conn.commit()
            return conn
    except (Exception) as error:
        print(error)
    return conn

def add_patient(form: ImmutableMultiDict) -> None:
    conn = __connect(os.getenv('DB_PATH'))
    cur = conn.cursor()
    cur.execute(f"INSERT INTO patients(fullName, teeth, actions, price, comment, date) VALUES ('{form['fullName']}', '{form['teeth']}', '{form['actions']}', '{form['price']}', '{form['comment']}', '{__get_current_date()}')")
    conn.commit()
    cur.close()
    conn.close()

def update_patient(form: ImmutableMultiDict, id: str) -> None:
    conn = __connect(os.getenv('DB_PATH'))
    cur = conn.cursor()
    cur.execute(f"UPDATE patients SET fullname='{form['fullName']}', teeth='{form['teeth']}', actions='{form['actions']}', price='{form['price']}', comment='{form['comment']}', date='{form['date']}' WHERE id={id}")
    conn.commit()
    cur.close()
    conn.close()

def delete_patient(id: str):
    conn = __connect(os.getenv('DB_PATH'))
    cur = conn.cursor()
    cur.execute(f"DELETE FROM patients WHERE id = {id}")
    conn.commit()
    cur.close()
    conn.close()

def get_patients() -> list[object]:
    conn = __connect(os.getenv('DB_PATH'))
    cur = conn.cursor()
    cur.execute('SELECT id, fullName, teeth, actions, price, comment, date FROM patients')
    patients = __convert(cur.fetchall())
    cur.close()
    conn.close()
    return patients

def get_patient(id) -> object:
    conn = __connect(os.getenv('DB_PATH'))
    cur = conn.cursor()
    cur.execute(f'SELECT id, fullName, teeth, actions, price, comment, date FROM patients WHERE id = {id}')
    patient = __convert(cur.fetchall())[0]
    cur.close()
    conn.close()
    return patient

def __get_current_date() -> str:
    return datetime.today().strftime('%Y-%m-%d')

def __convert(db_list) -> list[object]:
    patients = []
    for id, fullName, teeth, actions, price, comment, date in db_list:
        patients.append({'id': id,
                     'fullname': fullName,
                     'teeth': teeth,
                     'actions': actions,
                     'price': price,
                     'comment': comment,
                     'date': date})
    return patients