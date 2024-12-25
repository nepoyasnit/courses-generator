import sqlite3

from src.orm.category import Category
from src.orm.user import User
from src.orm.course import Course
from src.orm.module import Module
from src.orm.lesson import Lesson
from src.orm.feedback import Feedback
from src.orm.quiz import Quiz
from src.orm.question import Question
from src.orm.prompt import Prompt
from src.orm.answer import Answer
from src.registration import hash_password

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()

user = User(conn, cursor)
category = Category(conn, cursor)
course = Course(conn, cursor)
module = Module(conn, cursor)
lesson = Lesson(conn, cursor)
feedback = Feedback(conn, cursor)
quiz = Quiz(conn, cursor)
question = Question(conn, cursor)
answer = Answer(conn, cursor)
prompt = Prompt(conn, cursor)

user.insert("maksim", "maksiksay@gmail.com", hash_password("11111111"))

category.insert("languages", "courses for languages")
category.insert("programming", "courses for programming")
category.insert("soft skills", "courses for better communication")


course.insert("English", "Best English Course", "english", "beginner", 1, 1)
course.insert("Python", "Best Python Course", "english", "beginner", 1, 1)
course.insert("Machine Learning", "ML4Life", "english", "advanced", 1, 1)


module.insert(1, "Intro", "Introduction in English", 1)
module.insert(1, "Learning", "Learn English", 2)

module.insert(2, "Intro", "Introduction in Python", 1)
module.insert(2, "Coding", "Learn Python", 2)

module.insert(3, "Intro", "Introduction in ML", 1)
module.insert(3, "Coding", "Learn ML", 2)

lesson.insert(1, "Letters", "Let's Learn some letters", 5, 1)
lesson.insert(1, "Words", "fsdfdsf", 10, 2)

feedback.insert(1, 1, 5, "Excellent course! Very informative.")
feedback.insert(1, 1, 4, "Great course, but could use more examples.")
feedback.insert(1, 2, 3, "The course was okay, but not very detailed.")
feedback.insert(1, 2, 2, "I found it difficult to follow the material.")

quiz.insert(1, "Python Basics Quiz")
quiz.insert(1, "Intermediate Python Quiz")

question.insert(1, "What is Python?", "short-answer")
question.insert(1, "Which of these is a Python data type? A) List B) Table C) Row", "multiple-choice")
question.insert(2, "Explain the concept of functions in Python.", "short-answer")
question.insert(2, "Which of these is a correct function declaration in Python? A) def func(): B) function func() {}", "multiple-choice")

answer.insert(1, "Programming Language", True)
answer.insert(2, "A", True)
answer.insert(3, "fdsdf", True)
answer.insert(4, "A", True)

prompt.insert("Course generator", "Prompt for course description", "Generate a detailed course description for a {course_difficulty} level course on {course_title} with {modules_amount} modules.")
prompt.insert("Module generator", "Prompt for module generation", "Generate a detailed module description for {module_number}th module with title {module_title} and with {lessons_amount} lessons in course {course_title}")
prompt.insert("Lesson generator", "Prompt for lesson generation", "Generate a detailed {lesson_number}th lesson with {lesson_title} title in module {module_title} in course {course_title}")
prompt.insert("Quiz generator", "Prompt for quiz generation", "Generate a quiz description for {lesson_title} lesson in in course {course_title} with {questions_amount} questions. You don't need to generate questions, only quiz description.")
prompt.insert("Question generator", "Prompt for question generation", "Generate a question description for {quiz_title} quiz in {lesson_title} lesson for course {course_title}")
prompt.insert("Answer generator", "Prompt for answer generation", "Generate an answer for question: {question}")
