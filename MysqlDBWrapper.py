import mysql.connector
from mysql.connector import Error

class MySQLDB:
    def __init__(self, config, prefix=""):
        """Initialize database connection using a configuration dictionary."""
        self.config = config
        self.prefix = prefix
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish the database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"],
                database=self.config["database"]
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("✅ Database connection established successfully.")
        except Error as e:
            print(f"❌ Connection failed: {e}")

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("🔌 Database connection closed.")

    def insert(self, table, data):
        table = self.prefix + table
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({keys}) VALUES ({values})"
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Insert failed: {e}")
            return None

    def update(self, table, data, where):
        table = self.prefix + table
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        where_clause = ' AND '.join([f"{key} = %s" for key in where.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        try:
            self.cursor.execute(sql, tuple(data.values()) + tuple(where.values()))
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Update failed: {e}")
            return None

    def select(self, table, where=None, columns='*', limit=None):
        table = self.prefix + table
        columns = ', '.join([f'`{col}`' for col in columns]) if isinstance(columns, (list, tuple)) else f'`{columns}`'
        sql = f"SELECT {columns} FROM `{table}`"
        values = ()
        if where:
            where_clause = ' AND '.join([f"`{key}` = %s" for key in where.keys()])
            sql += f" WHERE {where_clause}"
            values = tuple(where.values())
        if limit:
            sql += f" LIMIT {limit}"
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            return result        
        except Error as e:
            print(f"Select failed: {e}")
            return None

    def delete(self, table, where):
        table = self.prefix + table
        where_clause = ' AND '.join([f"{key} = %s" for key in where.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        try:
            self.cursor.execute(sql, tuple(where.values()))
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Delete failed: {e}")
            return None

    def raw_query(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Raw query failed: {e}")
            return None

    def start_transaction(self):
        self.connection.start_transaction()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()