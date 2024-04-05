from werkzeug.datastructures import ImmutableMultiDict
import sqlite3
import os
from util.language import get_svg_name_by_language

LIMIT = 10

def __connect(path_to_db: str):
    with sqlite3.connect(path_to_db) as conn:
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS patients(id INTEGER PRIMARY KEY, fullName NOT NULL, teeth, actions, price, comment, language, date)')
        conn.commit()
        return conn

def add_patient(form: ImmutableMultiDict) -> None:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f"INSERT INTO patients(fullName, teeth, actions, price, comment, language, date) VALUES ('{form['fullName']}', '{form['teeth']}', '{form['actions']}', '{form['price']}', '{form['comment']}', '{form['language']}', '{form['date']}')")
        conn.commit()
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()

def update_patient(form: ImmutableMultiDict, id: str) -> None:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f"UPDATE patients SET fullname='{form['fullName']}', teeth='{form['teeth']}', actions='{form['actions']}', price='{form['price']}', comment='{form['comment']}', language='{form['language']}', date='{form['date']}' WHERE id={id}")
        conn.commit()
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()

def delete_patient(id: str):
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f"DELETE FROM patients WHERE id = {id}")
        conn.commit()
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()

def get_patients(skip: str) -> list[object]:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'SELECT id, fullName, teeth, actions, price, comment, language, date FROM patients ORDER BY id DESC LIMIT {LIMIT} OFFSET {skip}')
        patients = __convert(cur.fetchall())
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
    return patients

def get_patients_by_full_name(full_name, skip) -> list[object]:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'SELECT id, fullName, teeth, actions, price, comment, language, date FROM patients WHERE fullName LIKE \'%{full_name}%\' ORDER BY id DESC LIMIT {LIMIT} OFFSET {skip}')
        patients = __convert(cur.fetchall())
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
    return patients

def get_patient(id) -> object:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'SELECT id, fullName, teeth, actions, price, comment, language, date FROM patients WHERE id = {id}')
        patient = __convert(cur.fetchall())[0]
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
    return patient

def get_patients_count() -> int:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM patients')
        count = cur.fetchone()[0]
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
    return count

def get_patients_by_full_name_count(full_name) -> int:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'SELECT COUNT(*) FROM patients WHERE fullName LIKE \'%{full_name}%\' ORDER BY id DESC')
        count = cur.fetchone()[0]
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
    return count

def __convert(db_list) -> list[object]:
    patients = []
    for id, fullName, teeth, actions, price, comment, language, date in db_list:
        patients.append({'id': id,
                     'fullname': fullName,
                     'teeth': teeth,
                     'actions': actions,
                     'price': price,
                     'comment': comment,
                     'language': language,
                     'lang_svg': get_svg_name_by_language(language),
                     'date': date})
    return patients