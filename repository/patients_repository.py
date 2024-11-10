from werkzeug.datastructures import ImmutableMultiDict
import sqlite3
import os
from util.language import get_svg_name_by_language
from util.log_config import load_log_config


logger = load_log_config("patients_repository")
LIMIT = 10


def __connect(path_to_db: str):
    with sqlite3.connect(path_to_db) as conn:
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS patients(id INTEGER PRIMARY KEY, fullName NOT NULL, teeth, actions, price, comment, language, phone, date, user_id)')
        conn.commit()
        return conn


def add_patient(form: ImmutableMultiDict, user_id: int) -> None:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO 
                    patients(fullName, teeth, actions, price, comment, language, phone, date, user_id) 
                    VALUES ('{form['fullName']}', '{form['teeth']}', '{form['actions']}', 
                    '{form['price']}', '{form['comment']}', '{form['language']}', 
                    '{form['phone']}', '{form['date']}', {user_id})''')
        conn.commit()
        logger.info(f"The doctor with id {str(user_id)} save patient successfully")
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} 
                     didn't save patient successfully. The error is: {error}''')
    finally:
        cur.close()
        conn.close()


def update_patient(form: ImmutableMultiDict, id: str, user_id: int) -> None:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''UPDATE patients 
                    SET fullname='{form['fullName']}', teeth='{form['teeth']}', actions='{form['actions']}',
                      price='{form['price']}', comment='{form['comment']}', language='{form['language']}', 
                      phone='{form['phone']}', date='{form['date']}' 
                    WHERE id = {id} and user_id = {user_id}''')
        conn.commit()
        logger.info(f"The doctor with id {str(user_id)} update patient successfully")
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} 
                     didn't update patient successfully. The error is: {error}''')
    finally:
        cur.close()
        conn.close()


def delete_patient(id: str, user_id: int):
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''DELETE FROM patients 
                    WHERE id = {id} and user_id = {user_id}''')
        conn.commit()
        logger.info(f"The doctor with id {str(user_id)} delete patient with id {id} successfully")
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} 
                     didn't delete patient with id {id} successfully. The error is: {error}''')
    finally:
        cur.close()
        conn.close()


def get_patients(user_id: int, skip: str) -> list[object]:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT DISTINCT
                    p.id, p.fullName, p.teeth, p.actions, p.price, p.comment, p.language, p.phone, STRFTIME('%d/%m/%Y', p.date)
                    FROM patients p 
                    JOIN users u ON p.user_id={user_id}
                    ORDER BY p.id 
                    DESC 
                    LIMIT {LIMIT} 
                    OFFSET {skip}''')
        patients = __convert(cur.fetchall())
        logger.info(f'''The doctor with id {str(user_id)} got patients successfully. 
                    The skip parameter is {skip}''')
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} didn't get patients successfully. 
                    The skip parameter is {skip}. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return patients


def get_patients_by_full_name(full_name, skip, user_id: int) -> list[object]:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT DISTINCT p.id, p.fullName, p.teeth, p.actions, p.price, p.comment, p.language, p.phone, STRFTIME('%d/%m/%Y', p.date) 
                    FROM patients p
                    JOIN users u ON p.user_id={user_id}
                    WHERE p.fullName LIKE \'%{full_name}%\' 
                    ORDER BY p.id DESC LIMIT {LIMIT} 
                    OFFSET {skip}''')
        patients = __convert(cur.fetchall())
        logger.info(f'''The doctor with id {str(user_id)} got patients successfully 
                    by full name -> {full_name}. The skip parameter is {skip}''')
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} didn't get patients successfully 
                    by full name -> {full_name}. The skip parameter is {skip}. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return patients


def get_patient(id, user_id: int) -> object:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT p.id, p.fullName, p.teeth, p.actions, p.price, p.comment, p.language, p.phone, p.date 
                    FROM patients p
                    JOIN users u ON p.user_id={user_id}
                    WHERE p.id = {id}''')
        patient = __convert(cur.fetchall())[0]
        logger.info(f"The doctor with id {str(user_id)} got patient with id {str(id)} successfully")
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} didn't get 
                     patient with id {str(id)} successfully. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return patient


def get_patients_count(user_id: int) -> int:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT COUNT(*) 
                    FROM patients p 
                    WHERE user_id={user_id}''')
        count = cur.fetchone()[0]
        logger.info(f"The doctor with id {str(user_id)} got patient's count -> {str(count)}")
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} didn't get 
                     patient's count successfully. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return count


def get_patients_by_full_name_count(full_name, user_id: int) -> int:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT COUNT(*) 
                    FROM patients p
                    WHERE p.fullName 
                    LIKE \'%{full_name}%\'
                    AND p.user_id={user_id} 
                    ORDER BY p.id DESC''')
        count = cur.fetchone()[0]
        logger.info(f'''The doctor with id {str(user_id)} 
                    got patient's count by full name -> 
                    count: {str(count)}, full name: {full_name}''')
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} didn't get patient's count 
                     by full name '{full_name}' successfully. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return count


def get_patients_by_actions(actions: str, skip: int, user_id: int) -> list[object]:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT DISTINCT p.id, p.fullName, p.teeth, p.actions, p.price, p.comment, p.language, p.phone, STRFTIME('%d/%m/%Y', p.date) 
                    FROM patients p
                    JOIN users u ON p.user_id={user_id}
                    WHERE p.actions LIKE \'%{actions}%\' 
                    ORDER BY p.id DESC LIMIT {LIMIT} 
                    OFFSET {skip}''')
        patients = __convert(cur.fetchall())
        logger.info(f'''The doctor with id {str(user_id)} 
                    got patients by actions successfully -> 
                    skip: {str(skip)}, actions: {actions}''')
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} 
                    didn't get patients by actions successfully -> 
                    skip: {str(skip)}, actions: {actions}. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return patients


def get_patients_by_actions_count(actions, user_id: int) -> int:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT COUNT(*) 
                    FROM patients p
                    WHERE p.actions 
                    LIKE \'%{actions}%\'
                    AND p.user_id={user_id}
                    ORDER BY p.id DESC''')
        count = cur.fetchone()[0]
        logger.info(f'''The doctor with id {str(user_id)} 
                    got patient's count by actions successfully -> 
                    count: {str(count)}, actions: {actions}''')
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} didn't get 
                    patient's count by actions successfully -> 
                    count: {str(count)}, actions: {actions}. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return count


def get_patients_by_date(date, skip, user_id: int) -> list[object]:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT DISTINCT p.id, p.fullName, p.teeth, p.actions, p.price, p.comment, p.language, p.phone, STRFTIME('%d/%m/%Y', p.date) 
                    FROM patients p
                    JOIN users u ON p.user_id={user_id}
                    WHERE p.date = '{date}'
                    ORDER BY p.id DESC LIMIT {LIMIT} 
                    OFFSET {skip}''')
        patients = __convert(cur.fetchall())
        logger.info(f'''The doctor with id {str(user_id)} got patients successfully 
                    by date -> {date}. The skip parameter is {skip}''')
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} didn't get patients successfully 
                    by date -> {date}. The skip parameter is {skip}. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return patients


def get_patients_by_date_count(date, user_id: int) -> int:
    try:
        conn = __connect(os.getenv('DB_PATH'))
        cur = conn.cursor()
        cur.execute(f'''SELECT COUNT(*) 
                    FROM patients p
                    WHERE p.date 
                    LIKE \'%{date}%\'
                    AND p.user_id={user_id}
                    ORDER BY p.id DESC''')
        count = cur.fetchone()[0]
        logger.info(f'''The doctor with id {str(user_id)} 
                    got patient's count by date successfully -> 
                    count: {str(count)}, date: {date}''')
    except (Exception) as error:
        logger.error(f'''The doctor with id {str(user_id)} didn't get 
                    patient's count by date successfully -> 
                    count: {str(count)}, date: {date}. The error is: {error}''')
    finally:
        cur.close()
        conn.close()
    return count


def __convert(db_list) -> list[object]:
    patients = []
    for id, fullName, teeth, actions, price, comment, language, phone, date in db_list:
        patients.append({'id': id,
                         'fullname': fullName,
                         'teeth': teeth,
                         'actions': actions,
                         'price': price,
                         'comment': comment,
                         'language': language,
                         'lang_svg': get_svg_name_by_language(language),
                         'phone': phone,
                         'date': date})
    return patients
