
def print_classes(data):
	for obj in data:
		if obj:
			obj.print_values()


def check_key(key: int) -> bool:
	if not isinstance(key, int):
		return False
	if key < 100 or key > 200:
		return False
	return True

def check_location(location: str)  -> bool:
	if not isinstance(location, str):
		return False
	gates = ['A', 'B', 'C', 'D', 'E', 'H', 'G']
	if not location.startswith("Gate "):
		return False
	for gate in gates:
		if location[5:] == gate:
			return True
	return False

def check_status(status: str) -> bool:
	if not isinstance(status, str):
		return False
	if status != "active" and status != "inactive":
		return False
	return True

def validate_tag(tag: dict):
	id, location,status = tag["id"], tag["location"], tag["status"]
	if not check_key(id):
		print(f"Invalid id: {id}")
		return None
	if not check_location(location):
		print(f"Invalid location: {location}")
		return None
	if not check_status(status):
		print(f"Invalid status: {status}")
		return None
	return id, location, status