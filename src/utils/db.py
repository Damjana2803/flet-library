import sqlite3, hashlib, os, json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def db_init():
	conn = sqlite3.connect(os.getenv('DB_NAME'))

	cursor = conn.cursor()
	
	# Legacy Athena tables (keeping for compatibility)
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

	# New Library System Tables
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS library_books (
			id INTEGER PRIMARY KEY,
			title VARCHAR(255) NOT NULL,
			author VARCHAR(255) NOT NULL,
			isbn VARCHAR(50) UNIQUE NOT NULL,
			category VARCHAR(100),
			publication_year INTEGER,
			publisher VARCHAR(255),
			description TEXT,
			total_copies INTEGER DEFAULT 1,
			available_copies INTEGER DEFAULT 1,
			location VARCHAR(255),
			status VARCHAR(50) DEFAULT 'available',
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
		);
	''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS library_members (
			id INTEGER PRIMARY KEY,
			first_name VARCHAR(100) NOT NULL,
			last_name VARCHAR(100) NOT NULL,
			email VARCHAR(255) UNIQUE NOT NULL,
			phone VARCHAR(50),
			address TEXT,
			membership_number VARCHAR(50) UNIQUE NOT NULL,
			membership_type VARCHAR(50) DEFAULT 'regular',
			membership_status VARCHAR(50) DEFAULT 'active',
			membership_start_date DATE,
			membership_end_date DATE,
			max_loans INTEGER DEFAULT 5,
			current_loans INTEGER DEFAULT 0,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
		);
	''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS library_loans (
			id INTEGER PRIMARY KEY,
			book_id INTEGER NOT NULL,
			member_id INTEGER NOT NULL,
			loan_date DATE NOT NULL,
			due_date DATE NOT NULL,
			return_date DATE,
			status VARCHAR(50) DEFAULT 'active',
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			
			FOREIGN KEY (book_id) REFERENCES library_books(id),
			FOREIGN KEY (member_id) REFERENCES library_members(id)
		);
	''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS library_reservations (
			id INTEGER PRIMARY KEY,
			book_id INTEGER NOT NULL,
			member_id INTEGER NOT NULL,
			reservation_date DATE NOT NULL,
			expiry_date DATE NOT NULL,
			status VARCHAR(50) DEFAULT 'active',
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			
			FOREIGN KEY (book_id) REFERENCES library_books(id),
			FOREIGN KEY (member_id) REFERENCES library_members(id)
		);
	''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS library_users (
			id INTEGER PRIMARY KEY,
			email VARCHAR(255) UNIQUE NOT NULL,
			password_hash VARCHAR(255) NOT NULL,
			user_type VARCHAR(50) DEFAULT 'member',
			member_id INTEGER,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			
			FOREIGN KEY (member_id) REFERENCES library_members(id)
		);
	''')

	# Check if legacy data is already filled
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

	# Migrate JSON data to SQLite if it exists
	migrate_json_to_sqlite(cursor, conn)

	conn.close()

def migrate_json_to_sqlite(cursor, conn):
	"""Migrate data from JSON file to SQLite database"""
	json_file_path = "storage/library_data.json"
	
	# Check if migration has already been done
	cursor.execute("SELECT already_filled FROM state WHERE id=1")
	res = cursor.fetchone()
	
	# Check if library migration flag exists
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='library_migration_state'")
	if not cursor.fetchone():
		# Create migration state table
		cursor.execute('''
			CREATE TABLE library_migration_state (
				id INTEGER PRIMARY KEY,
				migration_completed TINYINT DEFAULT(0),
				migration_date DATETIME
			)
		''')
		cursor.execute("INSERT INTO library_migration_state (id, migration_completed) VALUES(1, 0)")
		conn.commit()
	
	# Check if migration is already completed
	cursor.execute("SELECT migration_completed FROM library_migration_state WHERE id=1")
	migration_state = cursor.fetchone()
	
	if migration_state and migration_state[0] == 1:
		print("Migration already completed, skipping...")
		return
	
	if not os.path.exists(json_file_path):
		print("No JSON file found to migrate")
		# Mark migration as completed even if no file exists
		cursor.execute("UPDATE library_migration_state SET migration_completed = 1, migration_date = ? WHERE id = 1", (datetime.now().isoformat(),))
		conn.commit()
		return
	
	try:
		with open(json_file_path, 'r', encoding='utf-8') as f:
			data = json.load(f)
		
		print("Starting migration from JSON to SQLite...")
		
		# Migrate books
		if 'books' in data and data['books']:
			print(f"Migrating {len(data['books'])} books...")
			for book in data['books']:
				cursor.execute('''
					INSERT OR IGNORE INTO library_books 
					(id, title, author, isbn, category, publication_year, publisher, description, 
					 total_copies, available_copies, location, status, created_at)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				''', (
					book.get('id'),
					book.get('title', ''),
					book.get('author', ''),
					book.get('isbn', ''),
					book.get('category', ''),
					book.get('publication_year'),
					book.get('publisher', ''),
					book.get('description', ''),
					book.get('total_copies', 1),
					book.get('available_copies', 1),
					book.get('location', ''),
					book.get('status', 'available'),
					book.get('created_at', datetime.now().isoformat())
				))
		
		# Migrate members
		if 'members' in data and data['members']:
			print(f"Migrating {len(data['members'])} members...")
			for member in data['members']:
				cursor.execute('''
					INSERT OR IGNORE INTO library_members 
					(id, first_name, last_name, email, phone, address, membership_number, 
					 membership_type, membership_status, membership_start_date, membership_end_date,
					 max_loans, current_loans, created_at, updated_at)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				''', (
					member.get('id'),
					member.get('first_name', ''),
					member.get('last_name', ''),
					member.get('email', ''),
					member.get('phone', ''),
					member.get('address', ''),
					member.get('membership_number', ''),
					member.get('membership_type', 'regular'),
					member.get('membership_status', 'active'),
					member.get('membership_start_date'),
					member.get('membership_end_date'),
					member.get('max_loans', 5),
					member.get('current_loans', 0),
					member.get('created_at', datetime.now().isoformat()),
					member.get('updated_at', datetime.now().isoformat())
				))
		
		# Migrate loans
		if 'loans' in data and data['loans']:
			print(f"Migrating {len(data['loans'])} loans...")
			for loan in data['loans']:
				cursor.execute('''
					INSERT OR IGNORE INTO library_loans 
					(id, book_id, member_id, loan_date, due_date, status)
					VALUES (?, ?, ?, ?, ?, ?)
				''', (
					loan.get('id'),
					loan.get('book_id'),
					loan.get('member_id'),
					loan.get('loan_date'),
					loan.get('due_date'),
					loan.get('status', 'active')
				))
		
		# Migrate reservations
		if 'reservations' in data and data['reservations']:
			print(f"Migrating {len(data['reservations'])} reservations...")
			for reservation in data['reservations']:
				cursor.execute('''
					INSERT OR IGNORE INTO library_reservations 
					(id, book_id, member_id, reservation_date, expiry_date, status)
					VALUES (?, ?, ?, ?, ?, ?)
				''', (
					reservation.get('id'),
					reservation.get('book_id'),
					reservation.get('member_id'),
					reservation.get('reservation_date'),
					reservation.get('expiry_date'),
					reservation.get('status', 'active')
				))
		
		# Migrate users
		if 'users' in data and data['users']:
			print(f"Migrating {len(data['users'])} users...")
			for user in data['users']:
				cursor.execute('''
					INSERT OR IGNORE INTO library_users 
					(email, password_hash, user_type, member_id)
					VALUES (?, ?, ?, ?)
				''', (
					user.get('email', ''),
					user.get('password_hash', ''),
					user.get('user_type', 'member'),
					user.get('member_id')
				))
		
		conn.commit()
		print("Migration completed successfully!")
		
		# Create backup of JSON file
		backup_path = json_file_path + '.backup'
		with open(backup_path, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=2, ensure_ascii=False)
		print(f"JSON backup created at: {backup_path}")
		
		# Mark migration as completed
		cursor.execute("UPDATE library_migration_state SET migration_completed = 1, migration_date = ? WHERE id = 1", (datetime.now().isoformat(),))
		conn.commit()
		
	except Exception as e:
		print(f"Error during migration: {e}")
		conn.rollback()

