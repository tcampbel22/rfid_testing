import sqlite3

try:
	conn = sqlite3.connect("rfid.db")
	cursor = conn.cursor()
	print("Database connection established")

	if not conn:
		cursor.execute('''CREATE TABLE countries(
					id INTEGER PRIMARY KEY,
					name TEXT NOT NULL
					)''')

		cursor.execute('''CREATE TABLE warehouses(
					id INTEGER PRIMARY KEY,
					total_tags INTEGER NOT NULL,
					country_id INTEGER NOT NULL,
					FOREIGN KEY (country_id) REFERENCES countries(id)
					)''')
		
		cursor.execute('''CREATE TABLE rfid_tags(
				id INTEGER PRIMARY KEY,
				status TEXT NOT NULL,
				warehouse_id INTEGER,
				country_id INTEGER,
				FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
				FOREIGN KEY (country_id) REFERENCES countries(id)
				)''')
	# cursor.execute('INSERT INTO rfid_tags VALUES (1, "active", 1, 1);')
	# cursor.execute('INSERT INTO rfid_tags VALUES (2, "active", 1, 1);')
	# try: 
	# 	conn.commit()
	# except sqlite3.Error as err:
	# 	conn.rollback()
	# 	print('Error: ', err)
	
	cursor.execute('select * from rfid_tags;')
	tags = cursor.fetchall()
	print(f'{tags}')
	query = 'select sqlite_version();'
	cursor.execute(query)
	result = cursor.fetchall()
	print(f'SQLite version is {result}')
	cursor.close()

except sqlite3.Error as err:
	print('Error:', err)

finally:
	if conn:
		conn.close()
		print("DB connection closed")
	