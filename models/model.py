import sqlite3


class Model:
    def __init__(self):
        self.__database_file = "databases/database.db"
        self.__conn = None
        
    def __open_db_connection(self):
        try:
            self.__conn = sqlite3.connect(self.__database_file)
            self.__conn.row_factory = sqlite3.Row
            self.__conn.execute("PRAGMA foreign_keys = ON;")  
            return self.__conn
        except sqlite3.Error as e:
            print(f"Failed to open database connection: {e}")
            return None

    def __query_one(self, query: str, *args):
        conn = self.__open_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, args)
            if query.strip().upper().startswith("SELECT"):
                return cursor
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return None
            
    def __query_many(self, query: str, *args):
        conn = self.__open_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.executemany(query, *args)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return None
            
    def __close_db_connection(self):
        if self.__conn:
            self.__conn.cursor().close()
            self.__conn.close()
            self.__conn = None
        
# Create
    def insert_one(self, query: str, *args) -> int:
        cursor = self.__query_one(query, *args)
        if cursor:
            last_row_id = cursor.lastrowid
            self.__close_db_connection()
            return last_row_id
        return 0
    
    def insert_many(self, query: str, *args) -> int:
        cursor = self.__query_many(query, *args)
        if cursor:
            rowcount = cursor.rowcount
            self.__close_db_connection()
            return rowcount
        return 0
    
# Read   
    def fetch_one(self, query: str, *args) -> dict|None:
        cursor = self.__query_one(query, *args)
        if cursor:
            row = cursor.fetchone()
            self.__close_db_connection()
            return dict(row) if row else None
        return None

    def fetch_all(self, query: str, *args) -> list[dict]|list:
        cursor = self.__query_one(query, *args)
        if cursor:
            rows = cursor.fetchall()
            self.__close_db_connection()
            return [dict(row) for row in rows]
        return []

# Update
    def update(self, query: str, *args) -> int:
        cursor = self.__query_one(query, *args)
        if cursor:
            rowcount = cursor.rowcount
            self.__close_db_connection()
            return rowcount
        return 0

# Delete
    def delete(self, query: str, *args) -> int:
        cursor = self.__query_one(query, *args)
        if cursor:
            rowcount = cursor.rowcount
            self.__close_db_connection()
            return rowcount
        return 0