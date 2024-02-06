from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime

# mock data
patients = [
    {'fullname': 'Безрукавий Сергій',
     'teeth': '16,17',
     'actions': 'реставрація, консультація',
     'price': 100.50,
     'date': '2024-02-05'},
     {'fullname': 'Пригара Іван',
     'teeth': '46',
     'actions': 'ендо',
     'price': 150,
     'date': '2024-02-06'},
     {'fullname': 'Шевцов Богдан',
     'teeth': '',
     'actions': 'чистка',
     'price': 70,
     'date': '2024-02-06'},
     {'fullname': 'Микита Валерія',
     'teeth': '21,22',
     'actions': 'реставрація',
     'price': 180,
     'date': '2024-02-11'},
     {'fullname': 'Шетеля Володимир',
     'teeth': '23',
     'actions': 'ендо',
     'price': 120,
     'date': '2024-02-11'},
     {'fullname': 'Форос Анатолій',
     'teeth': '34',
     'actions': 'ендо',
     'price': 150,
     'date': '2024-02-12'}
]

def add_patient(form: ImmutableMultiDict) -> None:
    patients.append({'fullname': form['fullName'],
                     'teeth': form['teeth'],
                     'actions': form['actions'],
                     'price': form['price'],
                     'date': __get_current_date()})

def get_patients() -> list[object]:
    return patients

def __get_current_date() -> str:
    return datetime.today().strftime('%Y-%m-%d')