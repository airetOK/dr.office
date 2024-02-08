DROP TABLE IF EXISTS patients;
CREATE TABLE patients(id INTEGER PRIMARY KEY, fullName NOT NULL, teeth, actions, price, date);
INSERT INTO patients(fullName, teeth, actions, price, date) VALUES 
	('Безрукавий Сергій', '16,17', 'реставрація, консультація', '100.50', '2024-02-05'),
	('Пригара Іван', '46', 'ендо', '150', '2024-02-06'),
	('Шевцов Богдан', '', 'чистка', '70', '2024-02-06'),
	('Микита Валерія', '21,22', 'реставрація', '180', '2024-02-11'),
	('Шетеля Володимир', '23', 'ендо', '120', '2024-02-11'),
	('Форос Анатолій', '34', 'ендо', '150', '2024-02-12');