
---

# **RFID Tag Management System Test**

For running integration tests using SQLite, Flask, and pytest.

---

## **Overview**

This project is a backend system for managing RFID tags, warehouses, and their associated data. It provides RESTful APIs for operations such as fetching, adding, and moving RFID tags between warehouses. The system is built using Python (Flask) and SQLite for database management.

---

## **Features**

### **Endpoints**
1. **Fetch All Tags**  
   - **URL**: `/tags`  
   - **Method**: `GET`  
   - **Description**: Retrieves all RFID tags from the database.  
   - **Response**:  
     - `200`: List of tags.  
     - `500`: Error fetching tags.

2. **Fetch Tag by ID**  
   - **URL**: `/get-tag/<int:id>`  
   - **Method**: `GET`  
   - **Description**: Retrieves a specific RFID tag by its ID.  
   - **Response**:  
     - `200`: Tag details.  
     - `404`: Tag not found.  
     - `500`: Error fetching the tag.

3. **Add a New Tag**  
   - **URL**: `/add-tag`  
   - **Method**: `POST`  
   - **Description**: Adds a new RFID tag to the database.  
   - **Request Body**:  
     ```json
     {
       "id": 1,
       "status": "inactive",
       "warehouse_id": 3,
       "country_id": 2
     }
     ```  
   - **Response**:  
     - `201`: Tag created successfully.  
     - `400`: Invalid request body.  
     - `404`: Warehouse or country not found.  
     - `409`: Duplicate tag ID.  
     - `500`: Error adding the tag.

4. **Move a Tag to a New Warehouse**  
   - **URL**: `/move-tag/<int:id>`  
   - **Method**: `POST`  
   - **Description**: Moves an RFID tag from one warehouse to another.  
   - **Request Body**:  
     ```json
     {
       "old_warehouse_id": 1,
       "new_warehouse_id": 2
     }
     ```  
   - **Response**:  
     - `201`: Tag moved successfully.  
     - `400`: Invalid request body or same warehouse.  
     - `404`: Tag or warehouse not found.  
     - `500`: Error moving the tag.

---

## **Code Overview**

### **1. `server.py`**
- Implements the Flask application.
- Defines endpoints for managing RFID tags and warehouses.
- Uses helper functions from server_utils.py for database operations.

### **2. server_utils.py**
- Contains utility functions for database operations:
  - `fetch_one`: Fetches a single row from the database.
  - `fetch_all`: Fetches all rows from the database.
  - `execute_sql`: Executes an SQL statement and commits changes.
  - `parse_body`: Validates and parses request payloads.
  - `check_id`: Validates the existence of IDs in specific tables.

### **3. test_class.py**
- Contains test cases for the API endpoints and utility functions.
- Uses `pytest` for testing.
- Includes tests for:
  - Adding tags.
  - Fetching tags.
  - Moving tags.
  - Handling invalid inputs and edge cases.

### **4. rfid.py**
- Implements a simple TCP server for handling RFID tag updates.
- Simulates an in-memory database (`rfid_db`) for RFID tag statuses.
- Functions:
  - `handle_rfid`: Toggles the status of an RFID tag.
  - `start_server`: Starts the TCP server.

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.8 or higher
- SQLite
- `pip` (Python package manager)

### **2. Installation**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### **3. Database Setup**
1. Ensure the SQLite database is set up with the required tables:
   - `rfid_tags`
   - `warehouses`
   - `countries`
2. Use the provided SQL scripts (if available) to initialize the database.

### **4. Run the Server**
Start the Flask server:
```bash
python server.py
```
The server will run on `http://127.0.0.1:5000`.

---

## **Testing**

### **1. Run Tests**
To run the test suite, use:
```bash
pytest tests/test_class.py
```

### **2. Test Cases**
- **Validations**:
  - Check valid/invalid keys, locations, and statuses.
- **API Tests**:
  - Add a new tag.
  - Handle duplicate tags.
  - Fetch tags (all and by ID).
  - Move tags between warehouses.
  - Handle invalid inputs and edge cases.

---

## **RFID Server**

### **File**: rfid.py
- **Purpose**: Simulates an RFID server for toggling the status of RFID tags.
- **Features**:
  - Maintains an in-memory database (`rfid_db`) for RFID tags.
  - Toggles the status of a tag between `IN_WAREHOUSE` and `OUT_WAREHOUSE`.
  - Listens for incoming connections on `127.0.0.1:8081`.

### **Usage**
1. Start the RFID server:
   ```bash
   python rfid.py
   ```
2. Connect to the server and send an RFID tag ID to toggle its status.

---

## **Error Handling**

### **Custom Errors**
- `DuplicateError`: Raised when a duplicate ID is found.
- `NotFoundError`: Raised when a required record is not found.
- `ValueError`: Raised for invalid request payloads.

### **HTTP Status Codes**
- `200`: Success.
- `201`: Resource created successfully.
- `400`: Bad request (e.g., invalid input).
- `404`: Resource not found.
- `409`: Conflict (e.g., duplicate resource).
- `500`: Internal server error.

---
