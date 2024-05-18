from werkzeug.datastructures import ImmutableMultiDict
import sqlite3
import os

from util.password_encryptor import PasswordEncryptor

password_encryptor = PasswordEncryptor()

def __connect(path_to_db: str):
    with sqlite3.connect(path_to_db) as conn:
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username NOT NULL UNIQUE, password NOT_NULL)')
        conn.commit()
        return conn

def add_user(form: ImmutableMultiDict) -> None:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO users(username, password) 
                    VALUES ('{form['username']}', '{ password_encryptor.encrypt(form['password']) }')''')
        conn.commit()
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()

def get_id_by_username(username: str) -> int:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM users WHERE username = '{username}'")
        res = cur.fetchone()[0]
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
    return res

def is_user_exists(username, password) -> object:
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
    except (Exception) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
    return is_user_exists