import pytest
import sqlite3
import repository.users_repository as ur
import os
import logging

from util.password_encryptor import PasswordEncryptor


logger = logging.getLogger(__name__)
DB_PATH = 'tests/repository/test.db'
password_encryptor = PasswordEncryptor()

@pytest.fixture
def get_repository():
    os.environ["DB_PATH"] = DB_PATH
    yield ur
    os.remove(DB_PATH)

def test_add_user(get_repository):
    get_repository.add_user({'id': 1, 'username': 'user', 'password': 'test'})
    get_repository.add_user({'id': 2, 'username': 'user2', 'password': 'test2'})
    assert 1 == __get_user(1)[0]
    assert 'user' == __get_user(1)[1]
    assert password_encryptor.encrypt('test') == __get_user(1)[2]
    assert 2 == __get_user(2)[0]
    assert 'user2' == __get_user(2)[1]
    assert password_encryptor.encrypt('test2') == __get_user(2)[2]

def test_get_id_by_username(get_repository):
    get_repository.add_user({'id': 1, 'username': 'user', 'password': 'test'})
    assert 1 == get_repository.get_id_by_username('user')

def test_get_id_by_username_not_found(get_repository):
    with pytest.raises(UnboundLocalError):
        get_repository.get_id_by_username('user')

def test_is_user_exists(get_repository):
    get_repository.add_user({'id': 1, 'username': 'user', 'password': 'test'})
    assert get_repository.is_user_exists('user', 'test')

def test_is_user_not_exists(get_repository):
    assert not get_repository.is_user_exists('not_found', '')


def __get_user(id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            res = cur.execute(f'SELECT id, username, password FROM users WHERE id = "{id}"')
            data = res.fetchone()
    except (Exception) as error:
        logger.error(error)
    return data