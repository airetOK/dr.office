import sqlite3
import os
from util.log_config import load_log_config


logger = load_log_config(__name__)

def upgrade_table(path_to_db):
    with sqlite3.connect(path_to_db) as conn:
        try:
            cur = conn.cursor()
            cur.execute('ALTER TABLE patients ADD COLUMN phone TEXT;')
            conn.commit()
        except Exception as e:
            logger.error(e)
        finally:
            cur.close()