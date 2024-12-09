import sqlite3

from src.orm.base_orm import BaseORM


class User(BaseORM):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)
        
    def insert(self, username, email, password_hash):
        insert_query = """
        INSERT INTO Users (username, email, password_hash)
        VALUES (?, ?, ?);
        """

        try:
            self.cursor.execute(insert_query, (username, email, password_hash))

            self.connection.commit()
            print(f"User '{username}' inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting user: {e}")
    
    def update(self, user_id, username=None, email=None, password_hash=None):
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
            self.cursor.execute(update_query, values)

            # Check if a row was updated
            if self.cursor.rowcount == 0:
                print(f"No user found with user_id {user_id}.")
            else:
                print(f"User with user_id {user_id} updated successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")

    def delete(self, user_id):
        delete_query = """
        DELETE FROM Users
        WHERE user_id = ?;
        """

        try:
            self.cursor.execute(delete_query, (user_id,))

            if self.cursor.rowcount == 0:
                print(f"No user found with user_id {user_id}.")
            else:
                print(f"User with user_id {user_id} deleted successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
