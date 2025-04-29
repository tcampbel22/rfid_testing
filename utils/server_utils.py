import sqlite3
from error.error_classes import *
def fetch_one(conn, sql, params=()):
	return conn.execute(sql, params).fetchone()

def fetch_all(conn, sql, params=()):
	return conn.execute(sql, params).fetchall()

def execute_sql(conn, sql, params=()):
	count = conn.execute(sql, params)
	conn.commit()
	return count.rowcount

def parse_body(body: dict, req_fields: dict):
	parsed = {}
	for key, cast in req_fields.items():
		if key not in body:
			raise ValueError(f'Error: {key} is missing from body')
		if key == "status" and body[key] != "active" and body[key] != "inactive":
			raise ValueError(f'Error: {key} should have a value of active or inactive only')
		try:
			parsed[key] = cast(body[key])
		except (ValueError, TypeError):
			raise ValueError(f'Error: {key} is of wrong type should be of type {cast}')
		if "id" in key and (int(body[key]) < 0 or int(body[key]) > 999999):
			raise ValueError(f'Error: {key} should have a value between 0 and 999999')
	return parsed

def check_id(conn, id, table):
	trusted_tables = ["rfid_tags", "warehouses", "countries"]
	if table not in trusted_tables:
		raise NotFoundError(f"Error: {table} table does not exist")
	data = conn.execute(f'SELECT id FROM {table} WHERE id = ?', (id,)).fetchone()
	if data and table == "rfid_tags":
		raise DuplicateError("Error: id already exists")
	if not data and table != "rfid_tags":
		raise NotFoundError(f'Error: id {id} does not exist in {table} table')




