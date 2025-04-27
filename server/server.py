from flask import Flask, jsonify, request
import sqlite3
from database.set_up import db_connection

app = Flask(__name__)

@app.route("/tags", methods=['GET'])
def get_tags():
	try:
		with db_connection() as conn:
			tags = conn.execute('SELECT * FROM rfid_tags;').fetchall()
			if not tags:
				return jsonify({'message': 'No tags found' }), 200
		return jsonify({
			'message': 'Tags successfully fetched', 
			'tags': [dict(tag) for tag in tags]}), 200
	except sqlite3.Error as err:
		print('Error:', err)
		return jsonify({'message': 'Tags could not be fetched'}), 500

@app.route("/get-tag/<int:id>", methods=['GET'])
def get_tag(id):
	try:
		with db_connection() as conn:
			tag = conn.execute('SELECT * FROM rfid_tags WHERE id = ?', (id,)).fetchone()
			if tag is None:
				return jsonify({'message': f'Tag {id} not found'}), 404
			return jsonify({'message': f'Tag {id} fetched successfully', "tag": dict(tag)}), 200
	except sqlite3.Error as err:
		print('Error:', err)
		return jsonify({'message': f'Tag {id} could not be fetched'}), 500


@app.route("/add-tag", methods=['POST'])
def add_tag():
	try:
		body = request.get_json()
		fields = ["id", "status", "warehouse_id", "country_id"]
		if not body or not all(field in body for field in fields):
			return jsonify({'message': 'Missing required field'}), 400
		if not isinstance(body['id'], int) or not isinstance(body['status'], str) or \
			not isinstance(body['warehouse_id'], int) or not isinstance(body['country_id'], int):
			return jsonify({'message': 'Invalid field type'}), 400

		with db_connection() as conn:
			dup_tag = conn.execute('SELECT id FROM rfid_tags WHERE id = ?', (body["id"],)).fetchone()
			if dup_tag:
				return jsonify({'message': 'Tag already exists'}), 409
			conn.execute('INSERT INTO rfid_tags (id, status, warehouse_id, country_id) VALUES (?, ?, ?, ?)', 
						(body['id'], body['status'], body['warehouse_id'], body['country_id']))
			conn.execute('UPDATE warehouses SET total_tags = total_tags + 1 WHERE id = ?', (body['warehouse_id'],))
			conn.commit()
		return jsonify({'message': 'Tag created successfully'}), 201
	except sqlite3.Error as err:
		print('Error:', err)
		return jsonify({'message': 'Failed to add tag'}, str(err)), 500

# Need to add more concise error handling and wrapper functions to keep it clean

@app.route("/move-tag/<int:id>", methods=['POST'])
def move_tag(id):
	try:
		body = request.get_json()
		fields = ["old_warehouse_id", "new_warehouse_id"]
		# Check if all fields exist
		if not body or not all(field in body for field in fields):
			return jsonify({'message': 'Missing fields in request'}), 400

		# Check if all the fields are the correct type
		if not isinstance(body['old_warehouse_id'], int) or not isinstance(body['new_warehouse_id'], int):
			return jsonify({"message": 'Body values are incorrect types, should be int'}), 400
		# 1 Check if tag exists
		# 2 Find new country id and store if, also check if the country exists
		# 3 Update tags warehouse id, plus update the totals for both warehouses
		with db_connection() as conn:
			tag = conn.execute('SELECT id FROM rfid_tags WHERE id = ?', (id,)).fetchone()
			if not tag:
				return jsonify({'message': f'Tag {id} not found'}), 404
		
			new_country_row = conn.execute('SELECT country_id FROM warehouses WHERE id = ?', (body["new_warehouse_id"],)).fetchone()
			if not new_country_row:
				return jsonify({'message': f'Warehouse {body["new_warehouse_id"]} not found'}), 404
			new_country_id = new_country_row["country_id"]
			print(new_country_id)
			conn.execute('UPDATE rfid_tags SET warehouse_id = ?, country_id = ? WHERE id = ?', (body["new_warehouse_id"], new_country_id, id,))
			
			conn.execute('''UPDATE warehouses 
					SET total_tags = CASE
					 	WHEN total_tags - 1 < 0 THEN 0
						ELSE total_tags -1
					END 
					WHERE id = ?''', (body["old_warehouse_id"],))
			
			conn.execute('UPDATE warehouses SET total_tags = total_tags + 1 WHERE id = ?', (body["new_warehouse_id"],))
			new_tag_info = conn.execute('SELECT * FROM rfid_tags WHERE id = ?', (id,)).fetchone()
			return jsonify({
				'message': f'tag {id} successfully moved',
				'new_tag_info': dict(new_tag_info)
				}), 201
	except sqlite3.Error as err:
		print("Unexpected Error:")
		print(f"URL: {request.url}")
		print(f"Body: {request.get_json()}")
		print(f"Error: {str(err)}")
		return jsonify({'message': f'Failed to move tag {id}', "error": f'{str(err)}'}), 500



# @app.route("/add-country", methods=['POST'])
# def add_country():
# 	return

if __name__ == '__main__':
		app.run(debug=True)

