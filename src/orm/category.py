import sqlite3

from src.orm.base_orm import BaseORM


class Category(BaseORM):
    def __init__(self):
        super().__init__()

    def insert(self, name, description):
        connection, cursor = self.db_connection()
        insert_query = """
        INSERT INTO Categories (name, description)
        VALUES (?, ?);
        """

        try:
            cursor.execute(insert_query, (name, description))
            connection.commit()
            print(f"Category '{name}' inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting category: {e}")

    def update(self, category_id, name=None, description=None):
        connection, cursor = self.db_connection()
        update_query = "UPDATE Categories SET "
        fields = []
        values = []

        if name:
            fields.append("name = ?")
            values.append(name)
        if description:
            fields.append("description = ?")
            values.append(description)

        # If no fields to update, exit the function
        if not fields:
            print("No fields to update.")
            return

        update_query += ", ".join(fields)
        update_query += " WHERE category_id = ?;"
        values.append(category_id)

        try:
            cursor.execute(update_query, values)

            if cursor.rowcount == 0:
                print(f"No category found with category_id {category_id}.")
            else:
                print(f"Category with category_id {category_id} updated successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating category: {e}")

    def delete(self, category_id):
        connection, cursor = self.db_connection()
        delete_query = """
        DELETE FROM Categories
        WHERE category_id = ?;
        """

        try:
            cursor.execute(delete_query, (category_id,))

            if cursor.rowcount == 0:
                print(f"No category found with category_id {category_id}.")
            else:
                print(f"Category with category_id {category_id} deleted successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting category: {e}")
