import sqlite3
from encryption import encrypt, decrypt


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("passwords.db")
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY,
                    service_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    notes TEXT
                )
            """)

    def add_password(self, service_name, username, password, notes=""):
        encrypted_password = encrypt(password)
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO passwords (service_name, username, password, notes)
                VALUES (?, ?, ?, ?)
            """,
                (service_name, username, encrypted_password, notes),
            )

    def get_passwords(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM passwords")
            return cursor.fetchall()
