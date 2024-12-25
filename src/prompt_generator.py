import sqlite3
import random

from src.model import Model
from src.orm.course import Course
from src.orm.module import Module
from src.orm.lesson import Lesson
from src.orm.quiz import Quiz
from src.orm.question import Question
from src.orm.answer import Answer
from src.orm.category import Category

chat = Model("Qwen/Qwen2.5-0.5B-Instruct", "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")

course = Course()
module = Module()
lesson = Lesson()
quiz = Quiz()
question = Question()
answer = Answer()
category = Category()

def output_generating(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful course generator. Your task is to generate courses, modules, lessons and quizes descriptions to teach user something new."},
        {"role": "user", "content": prompt}
    ]
    text = chat.tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = chat.tokenizer([text], return_tensors="pt").to(chat.model.device)
    generated_ids = chat.model.generate(
        **model_inputs,
        max_new_tokens=512
    )
    
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = chat.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return response


def generate_course_prompt(username: str, course_title: str, course_difficulty: str, course_category: str, modules_amount: int):
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    category = Category()

    base_prompt = f"Generate a detailed course description for a {course_difficulty} level course on {course_title} with category {course_category} with {modules_amount} modules."
    category.insert(course_category, course_category)

    cursor.execute("SELECT category_id FROM Categories WHERE name = ?", (course_category,))
    category = cursor.fetchone()
    if not category:
        print(f"Ошибка: Категория '{course_category}' не найдена.")
        return
    category_id = category[0]

    cursor.execute("SELECT user_id FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        print(f"Ошибка: Пользователь '{username}' не найден.")
        return
    user_id = user[0]

    course_result = output_generating(base_prompt)
    course.insert(course_title, course_result, "en", course_difficulty, category_id, user_id)
    return course_result


def generate_module_prompt(module_number: int, course_title: str, module_title: str, lessons_amount):
    base_prompt = f"Generate a detailed module description for {module_number}th module with title {module_title} and with {lessons_amount} lessons in course {course_title}"
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT course_id FROM Courses WHERE title = ?", (course_title,))
    course = cursor.fetchone()
    if not course:
        print(f"Ошибка: Курс '{course_title}' не найден.")
        
    course_id = course[0]

    cursor.execute("SELECT MAX(sequence) FROM Modules WHERE course_id = ?", (course_id,))
    max_sequence = cursor.fetchone()[0]
    if max_sequence is None:
        max_sequence = 0  # Если модулей еще нет, начинаем с 1
    
    sequence = max_sequence + 1

    module_description = output_generating(base_prompt)

    module.insert(course_id, course_title, module_description, sequence)
    return module_description


def generate_lesson_prompt(lesson_number: int, lesson_title, course_title: str, module_title: str):
    base_prompt = f"Generate a detailed {lesson_number}th lesson with {lesson_title} title in module {module_title} in course {course_title}."
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT module_id FROM Modules WHERE title = ?", (module_title,))
    module = cursor.fetchone()
    if not module:
        print(f"Ошибка: Модуль '{module_title}' не найден.")
        return
    module_id = module[0]
    
    cursor.execute("SELECT MAX(sequence) FROM Lessons WHERE module_id = ?", (module_id,))
    max_sequence = cursor.fetchone()[0]
    if max_sequence is None:
        max_sequence = 0  # Если уроков еще нет, начинаем с 1
    
    sequence = max_sequence + 1

    lesson_content = output_generating(base_prompt)


    lesson.insert(module_id, lesson_title, lesson_content, int(random.random()), sequence)
    return lesson_content

def generate_quiz_prompt(course_title: str, lesson_title: str, questions_amount):
    base_prompt = f"Generate a quiz title for {lesson_title} lesson in in course {course_title}. You don't need to generate questions, only quiz title no more that 3 tokens."
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT lesson_id FROM Lessons WHERE title = ?", (lesson_title,))
    lesson = cursor.fetchone()
    if not lesson:
        print(f"Ошибка: Урок '{lesson_title}' не найден.")
        return
    lesson_id = lesson[0]

    quiz_content = output_generating(base_prompt)

    quiz.insert(lesson_id, quiz_content)
    return quiz_content

def generate_question_prompt(quiz_title: str, course_title: str, lesson_title: str, question_type: str):
    base_prompt = f"Generate a question description for {quiz_title} quiz in {lesson_title} lesson for course {course_title}"
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT quiz_id FROM Quizzes WHERE title = ?", (quiz_title,))
    quiz = cursor.fetchone()
    if not quiz:
        print(f"Ошибка: Викторина '{quiz_title}' не найдена.")
        return
    quiz_id = quiz[0]

    question_content = output_generating(base_prompt)

    question.insert(quiz_id, question_content, question_type)
    return question_content

def generate_answer_prompt(question: str):
    base_prompt = f"Generate an answer for question: {question}"
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT question_id FROM Questions WHERE question_text = ?", (question,))
    question = cursor.fetchone()
    if not question:
        print(f"Вопрос '{question}' не найден.")
        question_id = 1
    else:
        question_id = question[0]

    answer_output = output_generating(base_prompt)

    answer.insert(question_id, answer_output, True)

