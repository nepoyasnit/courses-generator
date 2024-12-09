import sqlite3

from src.orm.base_orm import BaseORM


class Module(BaseORM):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    def insert(self, course_id, title, description, sequence):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        insert_query = """
        INSERT INTO Modules (course_id, title, description, sequence)
        VALUES (?, ?, ?, ?);
        """

        try:
            self.cursor.execute(insert_query, (course_id, title, description, sequence))
            self.connection.commit()
            print(f"Module '{title}' inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting module: {e}")

    def update(self, module_id, course_id=None, title=None, description=None, sequence=None):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        update_query = "UPDATE Modules SET "
        fields = []
        values = []

        if course_id:
            fields.append("course_id = ?")
            values.append(course_id)
        if title:
            fields.append("title = ?")
            values.append(title)
        if description:
            fields.append("description = ?")
            values.append(description)
        if sequence:
            fields.append("sequence = ?")
            values.append(sequence)

        if not fields:
            print("No fields to update.")
            return

        update_query += ", ".join(fields)
        update_query += " WHERE module_id = ?;"
        values.append(module_id)

        try:
            self.cursor.execute(update_query, values)

            if self.cursor.rowcount == 0:
                print(f"No module found with module_id {module_id}.")
            else:
                print(f"Module with module_id {module_id} updated successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating module: {e}")

    def delete(self, module_id):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # SQL command to delete data
        delete_query = """
        DELETE FROM Modules
        WHERE module_id = ?;
        """

        try:
            # Execute the delete command
            self.cursor.execute(delete_query, (module_id,))

            # Check if a row was deleted
            if self.cursor.rowcount == 0:
                print(f"No module found with module_id {module_id}.")
            else:
                print(f"Module with module_id {module_id} deleted successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting module: {e}")
