import sqlite3

from src.orm.base_orm import BaseORM


class Answer(BaseORM):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    def insert(self, question_id, answer_text, is_correct):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        insert_query = """
        INSERT INTO Answers (question_id, answer_text, is_correct)
        VALUES (?, ?, ?);
        """

        try:
            self.cursor.execute(insert_query, (question_id, answer_text, is_correct))
            self.connection.commit()
            print(f"Answer inserted successfully for question_id {question_id}.")
        except sqlite3.Error as e:
            print(f"Error inserting answer: {e}")
    
    def update(self, answer_id, question_id=None, answer_text=None, is_correct=None):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # Build the SQL query dynamically based on provided parameters
        update_query = "UPDATE Answers SET "
        fields = []
        values = []

        if question_id is not None:
            fields.append("question_id = ?")
            values.append(question_id)
        if answer_text:
            fields.append("answer_text = ?")
            values.append(answer_text)
        if is_correct is not None:
            fields.append("is_correct = ?")
            values.append(is_correct)

        if not fields:
            print("No fields to update.")
            self.connection.close()
            return

        update_query += ", ".join(fields)
        update_query += " WHERE answer_id = ?;"
        values.append(answer_id)

        try:
            self.cursor.execute(update_query, values)

            if self.cursor.rowcount == 0:
                print(f"No answer found with answer_id {answer_id}.")
            else:
                print(f"Answer with answer_id {answer_id} updated successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating answer: {e}")

    def delete(self, answer_id):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        delete_query = """
        DELETE FROM Answers
        WHERE answer_id = ?;
        """

        try:
            self.cursor.execute(delete_query, (answer_id,))

            if self.cursor.rowcount == 0:
                print(f"No answer found with answer_id {answer_id}.")
            else:
                print(f"Answer with answer_id {answer_id} deleted successfully.")

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error deleting answer: {e}")

