import sqlite3



def create_tables(cursor):
	cursor.execute("SELECT COUNT(*) FROM countries;")
	if  cursor.fetchone()[0] > 0:
		return
	create_countries_table = '''CREATE TABLE IF NOT EXISTS countries(
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					name TEXT NOT NULL UNIQUE
					)'''

	create_warehouses_table = '''CREATE TABLE IF NOT EXISTS warehouses(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL UNIQUE,
				total_tags INTEGER NOT NULL DEFAULT 0,
				country_id INTEGER NOT NULL,
				FOREIGN KEY (country_id) REFERENCES countries(id)
				)'''
	
	create_tags_table = '''CREATE TABLE IF NOT EXISTS rfid_tags(
			id INTEGER PRIMARY KEY,
			status TEXT NOT NULL,
			warehouse_id INTEGER,
			country_id INTEGER,
			FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
			FOREIGN KEY (country_id) REFERENCES countries(id)
			)'''
	cursor.execute(create_countries_table)
	cursor.execute(create_warehouses_table)
	cursor.execute(create_tags_table)
	print('countries, warehouses and rfid_tags tables created')


def populate_base_data(cursor):
	cursor.execute('SELECT COUNT(*) FROM countries;')
	if cursor.fetchone()[0] > 0:
		print('Base data already populated')
		return
	populate_db = ''' 
			INSERT INTO countries (name) VALUES ("Finland");
			INSERT INTO countries (name) VALUES ("Sweden");
			INSERT INTO countries (name) VALUES ("Germany");
			INSERT INTO warehouses (total_tags, name, country_id) VALUES (0, "Espoo", 1);
			INSERT INTO warehouses (total_tags, name, country_id) VALUES (0, "Stockholm", 2);
			INSERT INTO warehouses (total_tags, name, country_id) VALUES (0, "Berlin", 3);
			INSERT INTO warehouses (total_tags, name, country_id) VALUES (0, "Frankfurt", 3);
			'''
	cursor.executescript(populate_db)
	print('Base data added to db')

def db_connection():
	try:
		conn = sqlite3.connect("database/rfid.db")
		cursor = conn.cursor()
		cursor.execute("PRAGMA foreign_keys = ON;")
		print("Database connection established")
		cursor.execute('SELECT sqlite_version();')
		result = cursor.fetchall()
		print(f'SQLite version is {result}')
		conn.row_factory = sqlite3.Row

		create_tables(cursor)
		populate_base_data(cursor)
		conn.commit()

		cursor.close()
		return conn

	except sqlite3.Error as err:
		print('Error:', err)
		raise RuntimeError("Database not found")

	# finally:
	# 	if conn:
	# 		conn.close()
	# 		print("DB connection closed")
		