import sqlite3

from src.orm.base_orm import BaseORM


class Question(BaseORM):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    def insert(self, quiz_id, question_text, question_type):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # SQL command to insert data
        insert_query = """
        INSERT INTO Questions (quiz_id, question_text, question_type)
        VALUES (?, ?, ?);
        """

        try:
            # Execute the insert command
            self.cursor.execute(insert_query, (quiz_id, question_text, question_type))
            self.connection.commit()
            print(f"Question inserted successfully for quiz_id {quiz_id}.")
        except sqlite3.Error as e:
            print(f"Error inserting question: {e}")
    
    def update(self, question_id, quiz_id=None, question_text=None, question_type=None):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        update_query = "UPDATE Questions SET "
        fields = []
        values = []

        if quiz_id is not None:
            fields.append("quiz_id = ?")
            values.append(quiz_id)
        if question_text:
            fields.append("question_text = ?")
            values.append(question_text)
        if question_type:
            if question_type not in ['multiple-choice', 'short-answer']:
                print(f"Invalid question_type '{question_type}'. Must be 'multiple-choice' or 'short-answer'.")
                return
            fields.append("question_type = ?")
            values.append(question_type)

        # If no fields to update, exit the function
        if not fields:
            print("No fields to update.")
            return

        update_query += ", ".join(fields)
        update_query += " WHERE question_id = ?;"
        values.append(question_id)

        try:
            # Execute the update command
            self.cursor.execute(update_query, values)

            # Check if a row was updated
            if self.cursor.rowcount == 0:
                print(f"No question found with question_id {question_id}.")
            else:
                print(f"Question with question_id {question_id} updated successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating question: {e}")

    def delete(self, question_id):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        delete_query = """
        DELETE FROM Questions
        WHERE question_id = ?;
        """

        try:
            self.cursor.execute(delete_query, (question_id,))

            if self.cursor.rowcount == 0:
                print(f"No question found with question_id {question_id}.")
            else:
                print(f"Question with question_id {question_id} deleted successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting question: {e}")

