import sqlite3
from error.error_classes import *

# Fetch a single row from the database
def fetch_one(conn, sql, params=()):
    return conn.execute(sql, params).fetchone()

# Fetch all rows from the database
def fetch_all(conn, sql, params=()):
    return conn.execute(sql, params).fetchall()

# Execute an SQL statement and commit the changes
def execute_sql(conn, sql, params=()):
    count = conn.execute(sql, params)
    conn.commit()
    return count.rowcount

# Parse and validate the request body against required fields
def parse_body(body: dict, req_fields: dict):
    parsed = {}
    for key, cast in req_fields.items():
        # Check if the key is missing
        if key not in body:
            raise ValueError(f'Error: {key} is missing from body')
        # Validate the status field
        if key == "status" and body[key] not in ["active", "inactive"]:
            raise ValueError(f'Error: {key} should have a value of active or inactive only')
        try:
            # Cast the value to the required type
            parsed[key] = cast(body[key])
        except (ValueError, TypeError):
            raise ValueError(f'Error: {key} is of wrong type should be of type {cast}')
        # Validate ID fields
        if "id" in key and (int(body[key]) < 0 or int(body[key]) > 999999):
            raise ValueError(f'Error: {key} should have a value between 0 and 999999')
    return parsed

# Check if an ID exists in a specific table
def check_id(conn, id, table):
    # Define trusted tables to prevent SQL injection
    trusted_tables = ["rfid_tags", "warehouses", "countries"]
    if table not in trusted_tables:
        raise NotFoundError(f"Error: {table} table does not exist")
    # Query the database for the ID
    data = conn.execute(f'SELECT id FROM {table} WHERE id = ?', (id,)).fetchone()
    # Handle duplicate or missing IDs
    if data and table == "rfid_tags":
        raise DuplicateError("Error: id already exists")
    if not data and table != "rfid_tags":
        raise NotFoundError(f'Error: id {id} does not exist in {table} table')




