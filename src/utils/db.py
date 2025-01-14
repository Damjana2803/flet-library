import sqlite3, hashlib, os
from dotenv import load_dotenv

load_dotenv()

def db_init():
	conn = sqlite3.connect(os.getenv('DB_NAME'))

	cursor = conn.cursor()
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS faculties (
			id INTEGER PRIMARY KEY,
			name VARCHAR(50) NOT NULL
		);
	''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY,
			name TEXT NOT NULL,
			email VARCHAR(255) NOT NULL UNIQUE,
			password VARCHAR(255) NOT NULL,
			faculty_id INTEGER,
			is_admin TINYINT DEFAULT(0),
			
			FOREIGN KEY (faculty_id)
			REFERENCES faculties(id)
		);
	''')
	
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS sessions (
			id INTEGER PRIMARY KEY,
			token VARCHAR(255) NOT NULL UNIQUE,
			is_active TINYINT DEFAULT(1),
			valid_until DATETIME NOT NULL,
			users_id INT NOT NULL,
		
			FOREIGN KEY (users_id)
			REFERENCES users(id)
		);
	''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS meets (
			id INTEGER PRIMARY KEY,
			field TEXT NOT NULL,
			title VARCHAR(255) NOT NULL,
			description TEXT,
			location VARCHAR(255) NOT NULL,
			start_date DATE NOT NULL,
			start_time TIME NOT NULL,
			users_limit INT NOT NULL,
			created_by INT NOT NULL,
								
			FOREIGN KEY (created_by)
			REFERENCES users(id)
		);
	''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users_meets (
			id INT PRIMARY KEY,
			users_id INT NOT NULL,
			meets_id INT NOT NULL,
			comment STRING,
			comment_time DATETIME,
			stars INT,
								
			FOREIGN KEY (users_id)
			REFERENCES users(id),
			
			FOREIGN KEY (meets_id)
			REFERENCES meets(id)
		);
	''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS state (
			id INTEGER PRIMARY KEY,
			already_filled TINYINT DEFAULT(0)
		)
	''')

	cursor.execute("SELECT already_filled FROM state WHERE id=1")
	res = cursor.fetchone()
	
	if (res is None):
		cursor.execute("INSERT INTO state (id, already_filled) VALUES(1, 0)")
		conn.commit()

	if res is None or res[0] == 0:
		data = [
			(1, 'Ekonomski fakultet'), 
			(2, 'Medicinski fakultet'),
			(3, 'Poljoprivredni fakultet'),
			(4, 'Pravni fakultet'),
			(5, 'Prirodno-matematički fakultet'),
			(6, 'Učiteljski fakultet'),
			(7, 'Fakultet za sport i fizičko vaspitanje'),
			(8, 'Fakultet tehničkih nauka'),
			(9, 'Filozofski fakultet'),
		]
		cursor.executemany("INSERT INTO faculties VALUES (?, ?)", data)
		conn.commit()

		password = hashlib.sha256(b'admin').hexdigest()

		cursor.execute(f'''
			INSERT INTO users (id, name, email, password, is_admin) VALUES (1, 'Admin', 'admin@athena.com', '{password}', 1) 
		''') #insecure as hell, but who gives a damn...
		conn.commit()

		cursor.execute("UPDATE state SET already_filled = ? WHERE id = ?", (1, 1))
		conn.commit()

	conn.close()

