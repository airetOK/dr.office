import pytest
import sqlite3
import repository.patients_repository as pr
import os

DB_PATH = 'tests/repository/test.db'

@pytest.fixture
def get_repository():
    os.environ["DB_PATH"] = DB_PATH
    yield pr
    os.remove(DB_PATH)

def test_add_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    get_repository.add_patient({'fullName': 'test2', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    assert ('test', '11,12', 'test', '120', 'test', 'eng') == __get_patient(1)
    assert ('test2', '11,12', 'test', '120', 'test', 'eng') == __get_patient(2)

def test_update_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    get_repository.update_patient({'fullName': 'test2', 'teeth': '11,122', 'actions': 'test2', 'price': '1202', 'comment': 'test2', 'language': 'eng', 'date': '2024-01-01'} ,1)
    assert ('test2', '11,122', 'test2', '1202', 'test2', 'eng') == __get_patient(1)

def test_delete_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    get_repository.delete_patient(1)
    assert None == __get_patient(1)

def test_get_patients(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    get_repository.add_patient({'fullName': 'test2', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    get_repository.add_patient({'fullName': 'test2', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    assert 3 == len(get_repository.get_patients(skip=0))
    assert 0 == len(get_repository.get_patients(skip=3))

def test_get_patients_by_full_name(get_repository):
    get_repository.add_patient({'fullName': 'NameTest', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    get_repository.add_patient({'fullName': 'TestNameAgain', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    get_repository.add_patient({'fullName': 'AnotherTestName', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    assert 3 == len(get_repository.get_patients_by_full_name('Test', skip=0))
    assert 0 == len(get_repository.get_patients_by_full_name('Test', skip=3))
    assert 1 == len(get_repository.get_patients_by_full_name('Another', skip=0))
    assert 0 == len(get_repository.get_patients_by_full_name('unknown', skip=0))    

def test_get_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'date': '2024-01-01'})
    assert {'id': 1, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'unknown',
            'language': 'eng', 'date': '2024-01-01'} == get_repository.get_patient(1)
    
def test_get_patient_lang_svg(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Англійська', 'date': '2024-01-01'})
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Польська', 'date': '2024-01-01'})
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Українська', 'date': '2024-01-01'})
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': '', 'date': '2024-01-01'})
    assert {'id': 1, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'gbr',
            'language': 'Англійська', 'date': '2024-01-01'} == get_repository.get_patient(1)
    assert {'id': 2, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'pol',
            'language': 'Польська', 'date': '2024-01-01'} == get_repository.get_patient(2)
    assert {'id': 3, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'ukr',
            'language': 'Українська', 'date': '2024-01-01'} == get_repository.get_patient(3)
    assert {'id': 4, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'unknown',
            'language': '', 'date': '2024-01-01'} == get_repository.get_patient(4)

def test_get_patients_only_one_record_return(get_repository):
    for i in range(0, 20):
        get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': '', 'date': '2024-01-01'})
    
    assert 1 == len(get_repository.get_patients_by_full_name('test', skip=19))
    assert 10 == len(get_repository.get_patients_by_full_name('test', skip=5))


def __get_patient(id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            res = cur.execute(f'SELECT fullName, teeth, actions, price, comment, language FROM patients WHERE id = "{id}"')
            data = res.fetchone()
    except (Exception) as error:
        print(error)
    return data