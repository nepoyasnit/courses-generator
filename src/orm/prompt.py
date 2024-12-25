import sqlite3

from src.orm.base_orm import BaseORM


class Prompt(BaseORM):
    def __init__(self):
        super().__init__()

    def insert(self, prompt_type, title, description):
        connection, cursor = self.db_connection()
        insert_query = """
        INSERT INTO Prompts (prompt_type, title, description)
        VALUES (?, ?, ?);
        """

        try:
            cursor.execute(insert_query, (prompt_type, title, description))
            connection.commit()
            print(f"Prompt '{title}' inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting prompt: {e}")

    def update(self, prompt_id, prompt_type=None, title=None, description=None):
        connection, cursor = self.db_connection()
        update_query = "UPDATE Prompts SET "
        fields = []
        values = []

        if prompt_type:
            fields.append("prompt_type = ?")
            values.append(prompt_type)
        if title:
            fields.append("title = ?")
            values.append(title)
        if description:
            fields.append("description = ?")
            values.append(description)

        if not fields:
            print("No fields to update.")
            return

        update_query += ", ".join(fields)
        update_query += " WHERE prompt_id = ?;"
        values.append(prompt_id)

        try:
            cursor.execute(update_query, values)

            if cursor.rowcount == 0:
                print(f"No prompt found with prompt_id {prompt_id}.")
            else:
                print(f"Prompt with prompt_id {prompt_id} updated successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating prompt: {e}")

    def delete(self, prompt_id):
        connection, cursor = self.db_connection()
        delete_query = """
        DELETE FROM Prompts
        WHERE prompt_id = ?;
        """

        try:
            cursor.execute(delete_query, (prompt_id,))

            if cursor.rowcount == 0:
                print(f"No prompt found with prompt_id {prompt_id}.")
            else:
                print(f"Prompt with prompt_id {prompt_id} deleted successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting prompt: {e}")
