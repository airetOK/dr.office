import sqlite3
import os

from util.password_encryptor import PasswordEncryptor

def upgrade_table(path_to_db):
    with sqlite3.connect(path_to_db) as conn:
        try:
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username NOT NULL UNIQUE, password NOT_NULL)')
            conn.commit()
            cur.execute(f"INSERT INTO users(username, password) VALUES ('{os.getenv('JWT_USERNAME')}', '{PasswordEncryptor().encrypt(os.getenv('JWT_PASSWORD'))}')")
            conn.commit()
            cur.execute('ALTER TABLE patients ADD COLUMN user_id INTEGER REFERENCES users(id) default 1')
            conn.commit()
            cur.execute(f"INSERT INTO users(username, password) VALUES ('user2', 'test2')")
            conn.commit()
        except Exception as e:
            print(str(e))
        finally:
            cur.close()