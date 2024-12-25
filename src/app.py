import sqlite3
import gradio as gr

from src.registration import register_user, login_user
from src.orm.feedback import Feedback
from src.prompt_generator import generate_answer_prompt, generate_course_prompt, generate_lesson_prompt, \
                            generate_module_prompt, generate_question_prompt, generate_quiz_prompt

USER_EMAIL = ''

def login(email: str, password: str):
    global USER_EMAIL

    USER_EMAIL = login_user(email, password)
    
    return f"Welcome, {USER_EMAIL}!"

def register(username: str, email: str, password: str):
    global USER_EMAIL

    USER_EMAIL = register_user(username, email, password)
    return f"User {username} registered successfully!"

def generate_course(course_title: str, course_difficulty: str, course_category: str, modules_amount: int):
    global USER_EMAIL
    if USER_EMAIL == '':
        return "Error! Please register or log in"
    return generate_course_prompt(USER_EMAIL, course_title, course_difficulty, course_category, modules_amount)

def generate_module(module_number, course_title, module_title, lessons_amount):
    global USER_EMAIL
    if USER_EMAIL == "":
        return "Error! Please register or log in"
    return generate_module_prompt(module_number, course_title, module_title, lessons_amount)

def generate_lesson(lesson_number, lesson_title, course_title, module_title):
    global USER_EMAIL
    if USER_EMAIL == "":
        return "Error! Please register or log in"
    return generate_lesson_prompt(lesson_number, lesson_title, course_title, module_title)

def generate_quiz(course_title, lesson_title, questions_amount):
    global USER_EMAIL
    if USER_EMAIL == "":
        return "Error! Please register or log in"
    return generate_quiz_prompt(course_title, lesson_title, questions_amount)

def generate_question(quiz_title, course_title, lesson_title, question_type):
    global USER_EMAIL
    if USER_EMAIL == "":
        return "Error! Please register or log in"
    return generate_question_prompt(quiz_title, course_title, lesson_title, question_type)

def generate_answer(question):
    global USER_EMAIL
    if USER_EMAIL == "":
        return "Error! Please register or log in"
    return generate_answer_prompt(question)

def send_feedback(course_title, rating, comment):
    global USER_EMAIL
    if USER_EMAIL == "":
        return "Error! Please register or log in"
    
    feedback = Feedback()
    return feedback.add_feedback(USER_EMAIL, course_title, rating, comment)
    
with gr.Blocks() as app:
    with gr.Tab("Authorization"):
        gr.Markdown("# Login")
        with gr.Row():
            login_email = gr.Textbox(label="Login Email", placeholder="Enter your email...")
            login_password = gr.Textbox(label="Login Password", placeholder="Enter your password...")

            login_button = gr.Button("Login")


        gr.Markdown("# Register")
        with gr.Row():
            register_username = gr.Textbox(label="Register Username", placeholder="Create your username...")
            register_email = gr.Textbox(label="Register Email", placeholder="Enter your email...")
            register_password = gr.Textbox(label="Register Password", placeholder="Create your password...")
            
            register_button = gr.Button("Register")

        authorization_area = gr.Textbox(label="Authorization Output", placeholder="Your authorization output will be here...")
        
        login_button.click(
            fn=login, 
            inputs=[login_email, login_password], 
            outputs=authorization_area)
        
        register_button.click(
            fn=register, 
            inputs=[register_username, register_email, register_password], 
            outputs=authorization_area)


    with gr.Tab("Course Generator"):
        gr.Markdown("# 📚 Course Outline Generator")
        
        with gr.Row():
            topic_input = gr.Textbox(label="Course Topic", placeholder="e.g., Machine Learning, Art History")
            difficulty_dropdown = gr.Dropdown(choices=["beginner", "intermediate", "advanced"], label="Difficulty Level")
            modules_amount = gr.Number("Number of modules in course", minimum=1, maximum=10, step=1)
            course_category = gr.Textbox(label="Course Type", placeholder="e.g. Programming, Languages, Medicine, etc.")

        generate_button = gr.Button("Generate Course")
        
        output_area = gr.Textbox(label="Generated Course Outline", lines=20, placeholder="Your course outline will appear here.")

        generate_button.click(
            fn=generate_course, 
            inputs=[topic_input, difficulty_dropdown, course_category, modules_amount], 
            outputs=output_area)
        
    with gr.Tab("Module Generator"):
        gr.Markdown("# 📚 Module Outline Generator")
        
        with gr.Row():
            course_title = gr.Textbox(label="Course Title", placeholder="e.g. Programming, Languages, Medicine, etc.")
            module_title = gr.Textbox(label="Module Topic")
            module_number = gr.Number(label="Module number", minimum=1, maximum=10, step=1)
            lessons_amount = gr.Number(label="Lessons in module", minimum=1, maximum=10, step=1)

        module_button = gr.Button("Generate Module")
        
        module_output = gr.Textbox(label="Generated Module Outline", lines=20, placeholder="Your module outline will appear here.")

        module_button.click(
            fn=generate_module, 
            inputs=[module_number, course_title, module_title, lessons_amount], 
            outputs=module_output)

    with gr.Tab("Lesson Generator"):
        gr.Markdown("# 📚 Lesson Outline Generator")
        
        with gr.Row():
            lesson_course_title = gr.Textbox(label="Course Title", placeholder="e.g. Programming, Languages, Medicine, etc.")
            lesson_module_title = gr.Textbox(label="Module Title")
            lesson_title = gr.Textbox(label="Lesson Topic")
            lesson_number = gr.Number(label="Lesson number", minimum=1, maximum=10, step=1)

        lesson_button = gr.Button("Generate Lesson")
        
        lesson_output = gr.Textbox(label="Generated Lesson Outline", lines=20, placeholder="Your lesson outline will appear here.")

        lesson_button.click(
            fn=generate_lesson, 
            inputs=[lesson_number, lesson_title, lesson_course_title, lesson_module_title], 
            outputs=lesson_output)
        
    with gr.Tab("Quiz Generator"):
        gr.Markdown("# 📚 Quiz Outline Generator")
        
        with gr.Row():
            quiz_course_title = gr.Textbox(label="Course Title", placeholder="e.g. Programming, Languages, Medicine, etc.")
            quiz_lesson_title = gr.Textbox(label="Lesson Title")
            questions_amount = gr.Number(label="Questions amount", minimum=1, maximum=10, step=1)

        quiz_button = gr.Button("Generate Quiz")
        
        quiz_output = gr.Textbox(label="Generated Lesson Outline", lines=20, placeholder="Your quiz outline will appear here.")

        quiz_button.click(
            fn=generate_quiz, 
            inputs=[quiz_course_title, quiz_lesson_title, questions_amount], 
            outputs=quiz_output)

    with gr.Tab("Question Generator"):
        gr.Markdown("# 📚 Question Outline Generator")

        with gr.Row():
            question_course_title = gr.Textbox(label="Course Title", placeholder="e.g. Programming, Languages, Medicine, etc.")
            question_lesson_title = gr.Textbox(label="Lesson Title")
            question_quiz_title = gr.Textbox(label="Quiz Title")
            question_type = gr.Dropdown(choices=['multiple-choice', 'short-answer'], label="Question Type")

        question_button = gr.Button("Generate Question")
        
        question_output = gr.Textbox(label="Generated Question Outline", lines=20, placeholder="Your question outline will appear here.")

        question_button.click(
            fn=generate_question, 
            inputs=[question_quiz_title, question_course_title, question_lesson_title, question_type], 
            outputs=question_output)

    with gr.Tab("Answer Generator"):
        gr.Markdown("# 📚 Question-Answer Outline Generator")

        with gr.Row():
            question_text = gr.Textbox(label="Question Text", placeholder="Put your question here...")

        answer_button = gr.Button("Generate Answer")
        
        answer_output = gr.Textbox(label="Generated Answer Outline", lines=20, placeholder="Your answer outline will appear here.")

        answer_button.click(
            fn=generate_answer, 
            inputs=[question_text], 
            outputs=answer_output)

    with gr.Tab("Feedback"):
        gr.Markdown("# Reviews for courses")

        with gr.Row():
            with gr.Column():
                feedback_course_title = gr.Textbox(label="Course Title", placeholder="Put course name here...")
                feedback_rating = gr.Number(label="Ratng", minimum=1, maximum=5, step=1)
                feedback_comment = gr.Textbox(label="Feedback Text", placeholder="Put your review here...", lines=10)
            with gr.Column():
                feedback_result = gr.Textbox(label="Review result")
                feedback_button = gr.Button("Send feedback")  

                feedback_button.click(send_feedback, inputs=[feedback_course_title, feedback_rating, feedback_comment], outputs=feedback_result)


# Launch the app
app.launch()
