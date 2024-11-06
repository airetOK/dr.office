import pytest
import sqlite3
import repository.patients_repository as pr
import repository.users_repository as ur
import os
from util.log_config import load_log_config


logger = load_log_config(__name__)
DB_PATH = 'tests/repository/test.db'

@pytest.fixture
def get_repository():
    os.environ["DB_PATH"] = DB_PATH
    ur.__connect(DB_PATH)
    ur.add_user({'username': 'user', 'password': 'test'})
    yield pr
    os.remove(DB_PATH)

def test_add_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'test2', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    assert ('test', '11,12', 'test', '120', 'test', 'eng', '123') == __get_patient(1)
    assert ('test2', '11,12', 'test', '120', 'test', 'eng', '123') == __get_patient(2)

def test_update_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.update_patient({'fullName': 'test2', 'teeth': '11,122', 'actions': 'test2', 
                                   'price': '1202', 'comment': 'test2', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1, 1)
    assert ('test2', '11,122', 'test2', '1202', 'test2', 'eng', '123') == __get_patient(1)

def test_delete_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.delete_patient(1, 1)
    assert None == __get_patient(1)

def test_get_patients(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'test2', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'test2', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    assert 3 == len(get_repository.get_patients(1, skip=0))
    assert 0 == len(get_repository.get_patients(1, skip=3))

def test_get_patients_by_full_name(get_repository):
    get_repository.add_patient({'fullName': 'NameTest', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'TestNameAgain', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'AnotherTestName', 'teeth': '11,12', 'actions': 'test', 'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    assert 3 == len(get_repository.get_patients_by_full_name('Test', user_id=1, skip=0))
    assert 0 == len(get_repository.get_patients_by_full_name('Test', user_id=1,skip=3))
    assert 1 == len(get_repository.get_patients_by_full_name('Another', user_id=1, skip=0))
    assert 0 == len(get_repository.get_patients_by_full_name('unknown', user_id=1, skip=0))    

def test_get_patient(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    assert {'id': 1, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'unknown',
            'language': 'eng', 'phone': '123', 'date': '2024-01-01'} == get_repository.get_patient(1, 1)
    
def test_get_patient_lang_svg(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Англійська', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Польська', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Українська', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': '', 'phone': '123', 'date': '2024-01-01'}, 1)
    assert {'id': 1, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'gbr',
            'language': 'Англійська', 'phone': '123', 'date': '2024-01-01'} == get_repository.get_patient(1, 1)
    assert {'id': 2, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'pol',
            'language': 'Польська', 'phone': '123', 'date': '2024-01-01'} == get_repository.get_patient(2, 1)
    assert {'id': 3, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'ukr',
            'language': 'Українська', 'phone': '123', 'date': '2024-01-01'} == get_repository.get_patient(3, 1)
    assert {'id': 4, 'fullname': 'test', 'teeth': '11,12', 
            'actions': 'test', 'price': '120', 'comment': 'test', 'lang_svg': 'unknown',
            'language': '', 'phone': '123', 'date': '2024-01-01'} == get_repository.get_patient(4, 1)

def test_get_patients_only_one_record_return(get_repository):
    for i in range(0, 20):
        get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': '', 'phone': '123', 'date': '2024-01-01'}, 1)
    
    assert 1 == len(get_repository.get_patients_by_full_name('test', user_id=1, skip=19))
    assert 10 == len(get_repository.get_patients_by_full_name('test', user_id=1, skip=5))


def test_get_patients_count(get_repository):
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Англійська', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Польська', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Українська', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'test', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'Українська', 'phone': '123', 'date': '2024-01-01'}, 2)
    assert 3 == get_repository.get_patients_count(user_id=1)
    assert 1 == get_repository.get_patients_count(user_id=2)


def test_get_patients_count_for_non_exist_user(get_repository):
    assert 0 == get_repository.get_patients_count(user_id=0)


def test_get_patients_by_actions(get_repository):
    get_repository.add_patient({'fullName': 'NameTest', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'TestNameAgain', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'AnotherTestName', 'teeth': '11,12', 'actions': 'test', 'price': '120', 
                                'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    assert 3 == len(get_repository.get_patients_by_actions('test', user_id=1, skip=0))
    assert 0 == len(get_repository.get_patients_by_actions('unknown_actions', user_id=1, skip=0))
    assert 1 == len(get_repository.get_patients_by_actions('test', user_id=1, skip=2))
    assert 0 == len(get_repository.get_patients_by_actions('test', user_id=0, skip=0))


def test_get_patients_by_actions_count(get_repository):
    get_repository.add_patient({'fullName': 'NameTest', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'TestNameAgain', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'AnotherTestName', 'teeth': '11,12', 'actions': 'other', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'NameTest', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'TestNameAgain', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    assert 4 == get_repository.get_patients_by_actions_count('test', 1)
    assert 1 == get_repository.get_patients_by_actions_count('other', 1)
    assert 0 == get_repository.get_patients_by_actions_count('unknown', 1)
    assert 0 == get_repository.get_patients_by_actions_count('test', 0)

def test_get_patients_by_full_name_count(get_repository):
    get_repository.add_patient({'fullName': 'NameTest', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'TestNameAgain', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'AnotherTestName', 'teeth': '11,12', 'actions': 'other', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'NameTest', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    get_repository.add_patient({'fullName': 'TestNameAgain', 'teeth': '11,12', 'actions': 'test', 
                                'price': '120', 'comment': 'test', 'language': 'eng', 'phone': '123', 'date': '2024-01-01'}, 1)
    assert 2 == get_repository.get_patients_by_full_name_count('NameTest', 1)
    assert 1 == get_repository.get_patients_by_full_name_count('AnotherTestName', 1)
    assert 0 == get_repository.get_patients_by_full_name_count('unknown', 1)
    assert 0 == get_repository.get_patients_by_full_name_count('NameTest', 0)


def __get_patient(id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            res = cur.execute(f'SELECT fullName, teeth, actions, price, comment, language, phone FROM patients WHERE id = "{id}"')
            data = res.fetchone()
    except (Exception) as error:
        logger.error(error)
    return data