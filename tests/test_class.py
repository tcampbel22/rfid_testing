from utils.utils import check_key, check_location, check_status, validate_tag
from utils.rfid import RFIDtag, rfid_data, create_classes
from database.set_up import db_connection
import requests
import random
import pytest
import unittest

# Fixture to provide the base URL for API requests
@pytest.fixture
def base_url():
    return "http://127.0.0.1:5000"

# Test the check_key function
def test_check_key():
    assert check_key("hello") is False  # Invalid key
    assert check_key(99) is False       # Invalid key
    assert check_key(101) is True       # Valid key
    assert check_key(200000000000) is False  # Invalid key (too large)

# Test the check_location function
def test_check_location():
    assert check_location("hello") is False  # Invalid location
    assert check_location(99) is False       # Invalid location
    assert check_location("Gate A") is True  # Valid location
    assert check_location("Gate C") is True  # Valid location

# Test the check_status function
def test_check_status():
    assert check_status("abc") is False      # Invalid status
    assert check_status("active") is True    # Valid status
    assert check_status("inactive") is True  # Valid status
    assert check_status(100) is False        # Invalid status

# Test adding a new tag
def test_add_tags(base_url):
    tag = {
        "id": random.randint(3, 200),
        "status": "inactive",
        "warehouse_id": 3,
        "country_id": 2
    }
    res = requests.post(f"{base_url}/add-tag", json=tag)
    assert res.status_code == 201  # Tag created successfully

# Test adding a duplicate tag
def test_dup_tags(base_url):
    tag = {
        "id": 1,
        "status": "inactive",
        "warehouse_id": 3,
        "country_id": 2
    }
    res = requests.post(f"{base_url}/add-tag", json=tag)
    assert res.status_code == 409  # Duplicate tag error

# Test adding a tag with invalid fields
def test_bad_field(base_url):
    tag = {
        "id_tag": 1,  # Invalid field name
        "status": "inactive",
        "warehouse_id": 3,
        "country_id": 2
    }
    res = requests.post(f"{base_url}/add-tag", json=tag)
    assert res.status_code == 400  # Bad request error

# Test fetching a non-existent tag
def test_missing_tag(base_url):
    res = requests.get(f"{base_url}/get-tag/999")
    assert res.status_code == 404  # Tag not found

# Test fetching an existing tag
def test_get_tag(base_url):
    res = requests.get(f"{base_url}/get-tag/1")
    assert res.status_code == 200  # Tag fetched successfully

# Test moving a tag to a new warehouse
def test_move_tag(base_url):
    tag = {
        "old_warehouse_id": 1,
        "new_warehouse_id": 2,
    }
    res = requests.post(f"{base_url}/move-tag/1", json=tag)
    assert res.status_code == 201  # Tag moved successfully

# Test moving a tag back to its original warehouse
def test_move_tag_back(base_url):
    tag = {
        "old_warehouse_id": 2,
        "new_warehouse_id": 1,
    }
    res = requests.post(f"{base_url}/move-tag/1", json=tag)
    assert res.status_code == 201  # Tag moved successfully

# Test moving a tag to an invalid warehouse
def test_move_invalid_warhouse(base_url):
    tag = {
        "old_warehouse_id": 5,
        "new_warehouse_id": 1,
    }
    res = requests.post(f"{base_url}/move-tag/1", json=tag)
    assert res.status_code == 404  # Warehouse not found

# Test fetching all tags
def test_get_all_tags(base_url):
    res = requests.get(f"{base_url}/tags")
    assert res.status_code == 200  # Tags fetched successfully
    data = res.json()
    assert isinstance(data, dict)  # Response should be a dictionary
    assert "tags" in data          # Response should contain "tags"
    assert isinstance(data["tags"], list)  # "tags" should be a list

