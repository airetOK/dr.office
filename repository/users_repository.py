from werkzeug.datastructures import ImmutableMultiDict
import sqlite3
import os
from util.log_config import load_log_config

from util.password_encryptor import PasswordEncryptor


logger = load_log_config("users_repository")
password_encryptor = PasswordEncryptor()


def __connect(path_to_db: str):
    with sqlite3.connect(path_to_db) as conn:
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username NOT NULL UNIQUE, password NOT_NULL)')
        conn.commit()
        return conn


def add_user(form: ImmutableMultiDict) -> None:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO users(username, password) 
                    VALUES ('{form['username']}', '{ password_encryptor.encrypt(form['password']) }')''')
        conn.commit()
        logger.info(f"The user \'{form['username']}\' was added successfully")
    except (Exception) as error:
        logger.error(f'''The user with name \'{form['username']}\' 
                     wasn't added successfully. The error is: {error}''')
    finally:
        cur.close()
        conn.close()


def get_id_by_username(username: str) -> int:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM users WHERE username = '{username}'")
        res = cur.fetchone()[0]
        logger.info(f"The id {str(res)} for user with name \'{username}\' was found successfully")
    except (Exception) as error:
        logger.error(f'''The user's id wasn't retrieved successfully 
                     for user with username \'{username}\'. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return res


def is_user_exists_with_username(username) -> bool:
    is_user_exists = False
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT EXISTS(SELECT 1 
                    FROM users 
                    WHERE username='{username}' 
                    LIMIT 1)''')
        if cur.fetchone()[0] != 0:
            is_user_exists = True
            logger.info(f"The user with name \'{username}\' was found successfully")
    except (Exception) as error:
        logger.error(f'''The user with name \'{username}\' 
                     wasn't found successfully. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return is_user_exists


def is_user_exists(username, password) -> bool:
    is_user_exists = False
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT EXISTS(SELECT 1 
                    FROM users 
                    WHERE username='{username}' and password='{password_encryptor.encrypt(password)}' 
                    LIMIT 1)''')
        if cur.fetchone()[0] != 0:
            is_user_exists = True
            logger.info(f"The user with name \'{username}\' was found successfully")
    except (Exception) as error:
        logger.error(f'''The user with name \'{username}\' and provided password
                     wasn't found successfully. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return is_user_exists

def set_password(username: str, password: str):
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''UPDATE users SET password="{password_encryptor.encrypt(password)}"
                    WHERE username="{username}"''')
        conn.commit()
        logger.info(f"The password for user with name \'{username}\' was changed successfully")
    except (Exception) as error:
        logger.error(f'''The password wasn't changed successfully 
                     for user with name \'{username}\'.The error is: {error}''')
    finally:
        cur.close()
        conn.close()