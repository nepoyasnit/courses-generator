import sqlite3

from src.orm.base_orm import BaseORM

class Lesson(BaseORM):
    def __init__(self):
        super().__init__()

    def insert(self, module_id, title, content, duration_minutes, sequence):
        connection, cursor = self.db_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")

        insert_query = """
        INSERT INTO Lessons (module_id, title, content, duration_minutes, sequence)
        VALUES (?, ?, ?, ?, ?);
        """

        try:
            cursor.execute(insert_query, (module_id, title, content, duration_minutes, sequence))
            connection.commit()
            print(f"Lesson '{title}' inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting lesson: {e}")

    def update(self, lesson_id, module_id=None, title=None, content=None, duration_minutes=None, sequence=None):
        connection, cursor = self.db_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")

        update_query = "UPDATE Lessons SET "
        fields = []
        values = []

        if module_id is not None:
            fields.append("module_id = ?")
            values.append(module_id)
        if title:
            fields.append("title = ?")
            values.append(title)
        if content:
            fields.append("content = ?")
            values.append(content)
        if duration_minutes is not None:
            fields.append("duration_minutes = ?")
            values.append(duration_minutes)
        if sequence is not None:
            fields.append("sequence = ?")
            values.append(sequence)

        if not fields:
            print("No fields to update.")
            connection.close()
            return

        update_query += ", ".join(fields)
        update_query += " WHERE lesson_id = ?;"
        values.append(lesson_id)

        try:
            cursor.execute(update_query, values)

            if cursor.rowcount == 0:
                print(f"No lesson found with lesson_id {lesson_id}.")
            else:
                print(f"Lesson with lesson_id {lesson_id} updated successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating lesson: {e}")

    def delete(self, lesson_id):
        connection, cursor = self.db_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")

        delete_query = """
        DELETE FROM Lessons
        WHERE lesson_id = ?;
        """

        try:
            cursor.execute(delete_query, (lesson_id,))

            if cursor.rowcount == 0:
                print(f"No lesson found with lesson_id {lesson_id}.")
            else:
                print(f"Lesson with lesson_id {lesson_id} deleted successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting lesson: {e}")
