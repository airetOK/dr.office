import sqlite3

query = '''DROP TABLE IF EXISTS users;
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username NOT NULL UNIQUE, password NOT_NULL);
    DROP TABLE IF EXISTS patients;
    CREATE TABLE IF NOT EXISTS 
    patients(id INTEGER PRIMARY KEY, fullName NOT NULL, teeth, actions, price, 
    comment, language, date, user_id INTEGER REFERENCES users(id));'''

with sqlite3.connect('patients.db') as conn:
    cur = conn.cursor()
    cur.executescript(query)
    conn.commit()
