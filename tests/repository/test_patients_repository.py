import pytest
import sqlite3
import repository.patients_repository as pr
import os
from datetime import datetime

DB_PATH = 'tests/repository/test.db'

@pytest.fixture
def get_repository():
    os.environ["DB_PATH"] = DB_PATH
    yield pr
    os.remove(DB_PATH)

def test_add_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test'})
    get_repository.add_patient({'fullName': 'test2', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test'})
    assert ('test', '11,12', 'test', '120', 'test') == __get_patient(1)
    assert ('test2', '11,12', 'test', '120', 'test') == __get_patient(2)

def test_update_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test'})
    get_repository.update_patient({'fullName': 'test2', 'teeth': '11,122', 'actions': 'test2', 'price': '1202', 'comment': 'test2', 'date': '2024-01-01'} ,1)
    assert ('test2', '11,122', 'test2', '1202', 'test2') == __get_patient(1)

def test_delete_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test'})
    get_repository.delete_patient(1)
    assert None == __get_patient(1)

def test_get_patients(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test'})
    get_repository.add_patient({'fullName': 'test2', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test'})
    get_repository.add_patient({'fullName': 'test2', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test'})
    assert 3 == len(get_repository.get_patients())

def test_get_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test'})
    assert {'id': 1, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 
            'date': datetime.today().strftime('%Y-%m-%d')} == get_repository.get_patient(1)


def __get_patient(id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            res = cur.execute(f'SELECT fullName, teeth, actions, price, comment FROM patients WHERE id = "{id}"')
            data = res.fetchone()
    except (Exception) as error:
        print(error)
    return data