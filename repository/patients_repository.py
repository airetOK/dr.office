from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
import psycopg2
from configuration.config import load_config


def connect():
    try:
        with psycopg2.connect(**load_config()) as conn:
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def add_patient(form: ImmutableMultiDict) -> None:
    conn = connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO public."patients"("fullName", teeth, actions, price, date) VALUES (%s, %s, %s, %s, %s)', 
                (form['fullName'], form['teeth'], form['actions'], form['price'], __get_current_date()))
    conn.commit()
    cur.close()
    conn.close()

def get_patients() -> list[object]:
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT id, "fullName", teeth, actions, price, date FROM public."patients"')
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