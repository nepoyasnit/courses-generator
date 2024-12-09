import sqlite3

from src.orm.base_orm import BaseORM


class Quiz(BaseORM):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    def insert(self, lesson_id, title):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        insert_query = """
        INSERT INTO Quizzes (lesson_id, title)
        VALUES (?, ?);
        """

        try:
            self.cursor.execute(insert_query, (lesson_id, title))
            self.connection.commit()
            print(f"Quiz '{title}' inserted successfully for lesson_id {lesson_id}.")
        except sqlite3.Error as e:
            print(f"Error inserting quiz: {e}")

    def update(self, quiz_id, lesson_id=None, title=None):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        update_query = "UPDATE Quizzes SET "
        fields = []
        values = []

        if lesson_id is not None:
            fields.append("lesson_id = ?")
            values.append(lesson_id)
        if title:
            fields.append("title = ?")
            values.append(title)

        if not fields:
            print("No fields to update.")
            return

        update_query += ", ".join(fields)
        update_query += " WHERE quiz_id = ?;"
        values.append(quiz_id)

        try:
            self.cursor.execute(update_query, values)

            if self.cursor.rowcount == 0:
                print(f"No quiz found with quiz_id {quiz_id}.")
            else:
                print(f"Quiz with quiz_id {quiz_id} updated successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating quiz: {e}")

    def delete(self, quiz_id):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # SQL command to delete data
        delete_query = """
        DELETE FROM Quizzes
        WHERE quiz_id = ?;
        """

        try:
            self.cursor.execute(delete_query, (quiz_id,))

            if self.cursor.rowcount == 0:
                print(f"No quiz found with quiz_id {quiz_id}.")
            else:
                print(f"Quiz with quiz_id {quiz_id} deleted successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting quiz: {e}")
