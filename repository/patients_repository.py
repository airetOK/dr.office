# mock data
patients = [
    {'fullname': 'Безрукавий Сергій',
     'teeth': '16,17',
     'action': 'реставрація, консультація',
     'price': 100.50,
     'date': '2024-02-05'},
     {'fullname': 'Пригара Іван',
     'teeth': '46',
     'action': 'ендо',
     'price': 150,
     'date': '2024-02-06'},
     {'fullname': 'Шевцов Богдан',
     'teeth': '',
     'action': 'чистка',
     'price': 70,
     'date': '2024-02-06'},
     {'fullname': 'Микита Валерія',
     'teeth': '21,22',
     'action': 'реставрація',
     'price': 180,
     'date': '2024-02-11'},
     {'fullname': 'Шетеля Володимир',
     'teeth': '23',
     'action': 'ендо',
     'price': 120,
     'date': '2024-02-11'},
     {'fullname': 'Форос Анатолій',
     'teeth': '34',
     'action': 'ендо',
     'price': 150,
     'date': '2024-02-12'}
]

def get_patients() -> list[object]:
    return patients