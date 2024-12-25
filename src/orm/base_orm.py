import sqlite3


class BaseORM:
    def __init__(self):
        pass

    def db_connection(self):
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()
        return conn, cursor
