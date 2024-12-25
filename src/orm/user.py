import sqlite3

from src.orm.base_orm import BaseORM


class User(BaseORM):
    def __init__(self):
        super().__init__()
        
    def insert(self, username, email, password_hash):
        connection, cursor = self.db_connection()
        insert_query = """
        INSERT INTO Users (username, email, password_hash)
        VALUES (?, ?, ?);
        """
        
        try:
            cursor.execute(insert_query, (username, email, password_hash))

            connection.commit()
            print(f"User '{username}' inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting user: {e}")
    
    def update(self, user_id, username=None, email=None, password_hash=None):
        connection, cursor = self.db_connection()
        update_query = "UPDATE Users SET "
        fields = []
        values = []

        if username:
            fields.append("username = ?")
            values.append(username)
        if email:
            fields.append("email = ?")
            values.append(email)
        if password_hash:
            fields.append("password_hash = ?")
            values.append(password_hash)

        # If no fields to update, exit the function
        if not fields:
            print("No fields to update.")
            return

        update_query += ", ".join(fields)
        update_query += " WHERE user_id = ?;"
        values.append(user_id)

        try:
            # Execute the update command
            cursor.execute(update_query, values)

            # Check if a row was updated
            if cursor.rowcount == 0:
                print(f"No user found with user_id {user_id}.")
            else:
                print(f"User with user_id {user_id} updated successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")

    def delete(self, user_id):
        connection, cursor = self.db_connection()
        delete_query = """
        DELETE FROM Users
        WHERE user_id = ?;
        """

        try:
            cursor.execute(delete_query, (user_id,))

            if cursor.rowcount == 0:
                print(f"No user found with user_id {user_id}.")
            else:
                print(f"User with user_id {user_id} deleted successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
