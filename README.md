# MySQL Database Wrapper for Python

## Overview
This is a lightweight MySQL database wrapper for Python that simplifies database interactions using MySQL Connector. It provides easy-to-use methods for CRUD operations, transactions, and query execution with prepared statements.

## Features
- Simple and secure MySQL database connection
- Support for `SELECT`, `INSERT`, `UPDATE`, and `DELETE`
- Query execution with prepared statements
- Transaction handling (commit & rollback)
- Automatic reconnection handling
- Fetch results as dictionaries for easy data manipulation

## Installation
Ensure you have **Python 3.x** installed.

### 1. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 2. Install Required Dependencies
```sh
pip install mysql-connector-python
```

## 3. Exiting Virtual Environment
If you used a virtual environment, exit it using:
```sh
deactivate
```

## Usage

### 1. Initialize the Database Connection
```python
from db_wrapper import Database

# Create a database instance
config = {
    "host": "localhost",
    "user": "root",
    "password": "yourpassword",
    "database": "yourdatabase"
}
db = Database(config)
```

### 2. Performing Queries

#### Selecting Data
```python
# Fetch all records from a table
result = db.select("users", columns=["id", "username"], limit=5)
print(result)
```

#### Inserting Data
```python
data = {"username": "john_doe", "email": "john@example.com"}
user_id = db.insert("users", data)
print(f"Inserted user with ID: {user_id}")
```

#### Updating Data
```python
update_data = {"email": "newemail@example.com"}
db.update("users", update_data, where={"id": 1})
print("User updated successfully")
```

#### Deleting Data
```python
db.delete("users", where={"id": 2})
print("User deleted successfully")
```

#### Executing a Raw Query
```python
query = "SELECT COUNT(*) as user_count FROM users"
result = db.raw_query(query)
print(result)
```

### 3. Transactions
```python
try:
    db.start_transaction()
    db.insert("orders", {"user_id": 1, "amount": 99.99})
    db.commit()
    print("Transaction committed successfully")
except Exception as e:
    db.rollback()
    print(f"Transaction failed: {e}")
```

## Exporting Data to CSV
```python
import csv

data = db.select("settings", columns=["id", "key"])
with open("settings_export.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Setting Name", "Setting Key"])
    for row in data:
        setting_name = f"Settings: {row['key'].replace('-', ' ')}"
        writer.writerow([setting_name, row["key"]])
print("Exported to settings_export.csv ✅")
```

## License
This project is open-source and free to use under the MIT License.

