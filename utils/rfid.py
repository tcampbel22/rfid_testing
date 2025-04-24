from utils import *

rfid_data = [
		{ "id": 101, "location": "Gate A", "status": "active" },
		{ "id": 102, "location": "ate B", "status": "active" },
		{ "id": 103, "location": "Gate D", "status": "alive" },
		{ "id": 204, "location": "Gate H", "status": "active" },
		{ "id": 105, "location": "Gate 1", "status": "active" },
		{ "id": 106, "location": "Gate g", "status": "active"},
		{ "id": 107, "location": "Gate G", "status": "active"},
		{ "id": 108, "location": "Gate A", "status": "active"},
		{ "id": 109, "location": "Gate C", "status": "active"},
		{ "id": 110, "location": "Gate D", "status": "active"},
		{ "id": 111, "location": "Gate A", "status": "active"},
		{ "id": 1112, "location": "Gate B", "status": "active"},
		{ "id": 112, "location": "Gate H", "status": "active"},
		{ "id": 113, "location": "Gate Z", "status": "active"},
		{ "id": 114, "location": "Gate C", "status": "active"},
		{ "id": 115, "location": "Gate D", "status": "active"},
		{ "id": 116, "location": "Gate M", "status": "active"}
	]


class RFIDtag:
	def __init__(self, tag_id, location, status):
		self.tag_id = tag_id
		self.location = location
		self.status = status
	
	def move(self, new_location):
		self.location = new_location

	def print_values(self):
		print(f"****TAG****\nid: {self.tag_id}\nlocation: {self.location}\nstatus: {self.status}")


def create_classes(rfid_data):
	class_arr = [None] * len(rfid_data)
	for index, tag in enumerate(rfid_data):
		tag_data = validate_tag(tag)
		if tag_data:
			id, location, status = tag_data
			class_arr[index] = RFIDtag(id, location, status)
	return class_arr

# data = create_classes(rfid_data)
# print_classes(data)