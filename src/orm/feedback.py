import sqlite3

from src.orm.base_orm import BaseORM


class Feedback(BaseORM):
    def __init__(self):
        super().__init__()

    def add_feedback(self, username, course_title, rating, comment):
        try:
            connection, cursor = self.db_connection()

            cursor.execute("SELECT user_id FROM Users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if not user:
                raise ValueError(f"Пользователь с именем '{username}' не найден.")
            user_id = user[0]

            cursor.execute("SELECT course_id FROM Courses WHERE title = ?", (course_title,))
            course = cursor.fetchone()
            if not course:
                raise ValueError(f"Курс с названием '{course_title}' не найден.")
            course_id = course[0]

            cursor.execute("""
                INSERT INTO Feedback (user_id, course_id, rating, comment)
                VALUES (?, ?, ?, ?)""",
                (user_id, course_id, rating, comment))

            connection.commit()
            return "Отзыв успешно добавлен!"

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
        except ValueError as e:
            print(e)
        finally:
            connection.close()


    def insert(self, user_id, course_id, rating, comment):
        connection, cursor = self.db_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")

        insert_query = """
        INSERT INTO Feedback (user_id, course_id, rating, comment)
        VALUES (?, ?, ?, ?);
        """

        try:
            cursor.execute(insert_query, (user_id, course_id, rating, comment))
            connection.commit()
            print(f"Feedback inserted successfully for user_id {user_id} and course_id {course_id}.")
        except sqlite3.Error as e:
            print(f"Error inserting feedback: {e}")
    
    def update(self, feedback_id, user_id=None, course_id=None, rating=None, comment=None):
        connection, cursor = self.db_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Build the SQL query dynamically based on provided parameters
        update_query = "UPDATE Feedback SET "
        fields = []
        values = []

        if user_id is not None:
            fields.append("user_id = ?")
            values.append(user_id)
        if course_id is not None:
            fields.append("course_id = ?")
            values.append(course_id)
        if rating is not None:
            if rating < 1 or rating > 5:
                print(f"Invalid rating '{rating}'. Must be between 1 and 5.")
                return
            fields.append("rating = ?")
            values.append(rating)
        if comment:
            fields.append("comment = ?")
            values.append(comment)

        # If no fields to update, exit the function
        if not fields:
            print("No fields to update.")
            return

        update_query += ", ".join(fields)
        update_query += " WHERE feedback_id = ?;"
        values.append(feedback_id)

        try:
            cursor.execute(update_query, values)

            if cursor.rowcount == 0:
                print(f"No feedback found with feedback_id {feedback_id}.")
            else:
                print(f"Feedback with feedback_id {feedback_id} updated successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating feedback: {e}")

    def delete(self, feedback_id):
        connection, cursor = self.db_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")

        delete_query = """
        DELETE FROM Feedback
        WHERE feedback_id = ?;
        """

        try:
            cursor.execute(delete_query, (feedback_id,))

            if cursor.rowcount == 0:
                print(f"No feedback found with feedback_id {feedback_id}.")
            else:
                print(f"Feedback with feedback_id {feedback_id} deleted successfully.")

            connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting feedback: {e}")
