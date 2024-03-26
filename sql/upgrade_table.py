import sqlite3

def upgrade_table(path_to_db):
    with sqlite3.connect(path_to_db) as conn:
        try:
            cur = conn.cursor()
            cur.execute('ALTER TABLE patients ADD COLUMN language TEXT default unknown')
            conn.commit()
        except Exception as e:
            print(str(e))
        finally:
            cur.close()