from utils.utils import check_key, check_location, check_status, validate_tag
from utils.rfid import RFIDtag, rfid_data, create_classes

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
