import sqlite3

from src.orm.base_orm import BaseORM

class Lesson(BaseORM):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    def insert(self, module_id, title, content, duration_minutes, sequence):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        insert_query = """
        INSERT INTO Lessons (module_id, title, content, duration_minutes, sequence)
        VALUES (?, ?, ?, ?, ?);
        """

        try:
            self.cursor.execute(insert_query, (module_id, title, content, duration_minutes, sequence))
            self.connection.commit()
            print(f"Lesson '{title}' inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting lesson: {e}")

    def update(self, lesson_id, module_id=None, title=None, content=None, duration_minutes=None, sequence=None):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

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
            self.connection.close()
            return

        update_query += ", ".join(fields)
        update_query += " WHERE lesson_id = ?;"
        values.append(lesson_id)

        try:
            self.cursor.execute(update_query, values)

            if self.cursor.rowcount == 0:
                print(f"No lesson found with lesson_id {lesson_id}.")
            else:
                print(f"Lesson with lesson_id {lesson_id} updated successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating lesson: {e}")

    def delete(self, lesson_id):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # SQL command to delete data
        delete_query = """
        DELETE FROM Lessons
        WHERE lesson_id = ?;
        """

        try:
            self.cursor.execute(delete_query, (lesson_id,))

            if self.cursor.rowcount == 0:
                print(f"No lesson found with lesson_id {lesson_id}.")
            else:
                print(f"Lesson with lesson_id {lesson_id} deleted successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting lesson: {e}")
