from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route("/get-tag/:id", methods=['GET'])


if __name__ == '__main__':
	app.run()


