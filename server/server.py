from flask import Flask, jsonify, request
import sqlite3
from database.set_up import db_connection
from utils.server_utils import *

app = Flask(__name__)

# Endpoint to fetch all RFID tags
@app.route("/tags", methods=['GET'])
def get_tags():
    try:
        with db_connection() as conn:
            tags = fetch_all(conn, 'SELECT * FROM rfid_tags;')
            if not tags:
                return jsonify({'message': 'No tags found'}), 200
        return jsonify({
            'message': 'Tags successfully fetched', 
            'tags': [dict(tag) for tag in tags]}), 200
    except sqlite3.Error as err:
        print("Unexpected Error:")
        print(f"URL: {request.url}")
        print(f"Body: {request.get_json()}")
        print(f"Error: {str(err)}")
        return jsonify({'message': 'Tags could not be fetched'}), 500

# Endpoint to fetch a specific RFID tag by ID
@app.route("/get-tag/<int:id>", methods=['GET'])
def get_tag(id):
    try:
        with db_connection() as conn:
            tag = fetch_one(conn, 'SELECT * FROM rfid_tags WHERE id = ?', (id,))
            if tag is None:
                return jsonify({'message': f'Tag {id} not found'}), 404
            return jsonify({'message': f'Tag {id} fetched successfully', "tag": dict(tag)}), 200
    except sqlite3.Error as err:
        print("Unexpected Error:")
        print(f"URL: {request.url}")
        print(f"Body: {request.get_json()}")
        print(f"Error: {str(err)}")
        return jsonify({'message': f'Tag {id} could not be fetched'}), 500

# Endpoint to add a new RFID tag
@app.route("/add-tag", methods=['POST'])
def add_tag():
    payload = {
        "id": int,
        "status": str,
        "warehouse_id": int,
        "country_id": int
    }
    try:
        body = request.get_json()
        try:
            parsed_body = parse_body(body, payload)
        except ValueError as err:
            return jsonify({"message": str(err)}), 400
        id = parsed_body["id"]
        status = parsed_body["status"]
        warehouse_id = parsed_body["warehouse_id"]
        country_id = parsed_body["country_id"]

        with db_connection() as conn:
			try:
				conn.execute('BEGIN TRANSACTION')
				try:
					check_id(conn, id, "rfid_tags")
					check_id(conn, warehouse_id, "warehouses")
					check_id(conn, country_id, "countries")
				except DuplicateError as err:
					return jsonify({'message': str(err)}), 409
				except NotFoundError as err:
					return jsonify({'message': str(err)}), 404
				except ValueError as err:
					return jsonify({'message': str(err)}), 400
				execute_sql(conn, 'INSERT INTO rfid_tags (id, status, warehouse_id, country_id) VALUES (?, ?, ?, ?)', 
							(id, status, warehouse_id, country_id))
				execute_sql(conn, 'UPDATE warehouses SET total_tags = total_tags + 1 WHERE id = ?', (warehouse_id,))
				return jsonify({'message': 'Tag created successfully'}), 201
			except Exception as err:
				conn.rollback()
				raise err
	except sqlite3.Error as err:
        print("Unexpected Error:")
        print(f"URL: {request.url}")
        print(f"Body: {request.get_json()}")
        print(f"Error: {str(err)}")
        return jsonify({'message': 'Failed to add tag'}, str(err)), 500

# Endpoint to move an RFID tag to a new warehouse
@app.route("/move-tag/<int:id>", methods=['POST'])
def move_tag(id):
    payload = {
        "old_warehouse_id": int,
        "new_warehouse_id": int
    }
    try:
        body = request.get_json()
        try:
            parsed_body = parse_body(body, payload)
        except ValueError as err:
            return jsonify({"message": str(err)}), 400
        old_warehouse_id = parsed_body["old_warehouse_id"]
        new_warehouse_id = parsed_body["new_warehouse_id"]
        if old_warehouse_id == new_warehouse_id:
            return jsonify({'message': 'tag cannot be moved to same warehouse'}), 400

        with db_connection() as conn:
            try:
                conn.execute("BEGIN TRANSACTION")
                try:
                    check_id(conn, id, "rfid_tags")
                    check_id(conn, old_warehouse_id, "warehouses")
                    check_id(conn, new_warehouse_id, "warehouses")
                except DuplicateError as err:
                    return jsonify({'message': str(err)}), 409
                except NotFoundError as err:
                    return jsonify({'message': str(err)}), 404

                new_country_row = fetch_one(conn, 'SELECT country_id FROM warehouses WHERE id = ?', (new_warehouse_id,))
                new_country_id = new_country_row["country_id"]
                execute_sql(conn, 'UPDATE rfid_tags SET warehouse_id = ?, country_id = ? WHERE id = ?', (new_warehouse_id, new_country_id, id,))
                
                execute_sql(conn, '''UPDATE warehouses 
                        SET total_tags = CASE
                            WHEN total_tags - 1 < 0 THEN 0
                            ELSE total_tags -1
                        END 
                        WHERE id = ?''', (old_warehouse_id,))
                
                execute_sql(conn, 'UPDATE warehouses SET total_tags = total_tags + 1 WHERE id = ?', (new_warehouse_id,))
                new_tag_info = fetch_one(conn, 'SELECT * FROM rfid_tags WHERE id = ?', (id,))
                return jsonify({
                    'message': f'tag {id} successfully moved',
                    'new_tag_info': dict(new_tag_info)
                    }), 201
            except Exception as err:
                conn.rollback()
                raise err
    except sqlite3.Error as err:
        print("Unexpected Error:")
        print(f"URL: {request.url}")
        print(f"Body: {request.get_json()}")
        print(f"Error: {str(err)}")
        return jsonify({'message': f'Failed to move tag {id}', "error": f'{str(err)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

