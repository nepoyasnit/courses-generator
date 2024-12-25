import sqlite3

from src.orm.base_orm import BaseORM

class Course(BaseORM):
    def __init__(self):
        super().__init__()


    def insert(self, title, description, language, level, category_id, created_by):
        connection, cursor = self.db_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")

        insert_query = """
        INSERT INTO Courses (title, description, language, level, category_id, created_by)
        VALUES (?, ?, ?, ?, ?, ?);
        """

        if level not in ['beginner', 'intermediate', 'advanced']:
            print(f"Invalid level '{level}'. Must be one of 'beginner', 'intermediate', 'advanced'.")
            return

        try:
            cursor.execute(insert_query, (title, description, language, level, category_id, created_by))

            connection.commit()
            print("Course inserted successfully with course_id:", cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error inserting course: {e}")

    def update(self, course_id, title=None, description=None, language=None, level=None, category_id=None, created_by=None):
        connection, cursor = self.db_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")

        update_query = "UPDATE Courses SET "
        fields = []
        values = []

        if title:
            fields.append("title = ?")
            values.append(title)
        if description:
            fields.append("description = ?")
            values.append(description)
        if language:
            fields.append("language = ?")
            values.append(language)
        if level:
            if level not in ['beginner', 'intermediate', 'advanced']:
                print(f"Invalid level '{level}'. Must be one of 'beginner', 'intermediate', 'advanced'.")
                return
            fields.append("level = ?")
            values.append(level)
        if category_id:
            fields.append("category_id = ?")
            values.append(category_id)
        if created_by:
            fields.append("created_by = ?")
            values.append(created_by)

        if not fields:
            print("No fields to update.")
            return

        update_query += ", ".join(fields)
        update_query += " WHERE course_id = ?;"
        values.append(course_id)

        try:
            cursor.execute(update_query, values)

            if cursor.rowcount == 0:
                print(f"No course found with course_id {course_id}.")
            else:
                print(f"Course with course_id {course_id} updated successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating course: {e}")

    def delete(self, course_id: int):
        connection, cursor = self.db_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")

        delete_query = """
        DELETE FROM Courses
        WHERE course_id = ?;
        """

        try:
            cursor.execute(delete_query, (course_id,))

            if cursor.rowcount == 0:
                print(f"No course found with course_id {course_id}.")
            else:
                print(f"Course with course_id {course_id} deleted successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting course: {e}")

