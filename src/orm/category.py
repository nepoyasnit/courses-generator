import sqlite3

from src.orm.base_orm import BaseORM


class Category(BaseORM):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)
        
    def insert(self, name, description):
        insert_query = """
        INSERT INTO Categories (name, description)
        VALUES (?, ?);
        """

        try:
            self.cursor.execute(insert_query, (name, description))
            self.connection.commit()
            print(f"Category '{name}' inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting category: {e}")

    def update(self, category_id, name=None, description=None):
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
            self.cursor.execute(update_query, values)

            if self.cursor.rowcount == 0:
                print(f"No category found with category_id {category_id}.")
            else:
                print(f"Category with category_id {category_id} updated successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating category: {e}")

    def delete(self, category_id):
        delete_query = """
        DELETE FROM Categories
        WHERE category_id = ?;
        """

        try:
            self.cursor.execute(delete_query, (category_id,))

            if self.cursor.rowcount == 0:
                print(f"No category found with category_id {category_id}.")
            else:
                print(f"Category with category_id {category_id} deleted successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting category: {e}")
