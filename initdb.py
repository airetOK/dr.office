import sqlite3

def init_db():
    with open('sql/test_init.sql', 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()

    conn = sqlite3.connect('patients.db')
    cur = conn.cursor()
    cur.executescript(sql_script)
    conn.commit()
    cur.close()
    conn.close()