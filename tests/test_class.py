from utils.utils import check_key, check_location, check_status, validate_tag
from utils.rfid import RFIDtag, rfid_data, create_classes
from database.set_up import db_connection
import requests
import random

BASE_URL = "http://127.0.0.1:5000"

def test_check_key():
	assert check_key("hello") is False
	assert check_key(99) is False
	assert check_key(101) is True
	assert check_key(200000000000) is False

def test_check_location():
	assert check_location("hello") is False
	assert check_location(99) is False
	assert check_location("Gate A") is True
	assert check_location("Gate C") is True

def test_check_status():
	assert check_status("abc") is False
	assert check_status("active") is True
	assert check_status("inactive") is True
	assert check_status(100) is False

def test_add_tags():
	tag = {
		"id": random.randint(3, 200),
		"status": "inactive",
		"warehouse_id": 3,
		"country_id": 2
	}
	res = requests.post(f"{BASE_URL}/add-tag", json=tag)
	assert res.status_code == 201

def test_dup_tags():
	tag = {
		"id": 1,
		"status": "inactive",
		"warehouse_id": 3,
		"country_id": 2
	}
	res = requests.post(f"{BASE_URL}/add-tag", json=tag)
	assert res.status_code == 409

def test_bad_field():
	tag = {
		"id_tag": 1,
		"status": "inactive",
		"warehouse_id": 3,
		"country_id": 2
	}
	res = requests.post(f"{BASE_URL}/add-tag", json=tag)
	assert res.status_code == 400

# def test_add_country


def test_get_all_tags():
	res = requests.get(f"{BASE_URL}/tags")
	assert res.status_code == 200
	data = res.json()
	assert isinstance(data, dict)
	assert "tags" in data
	assert isinstance(data["tags"], list)

