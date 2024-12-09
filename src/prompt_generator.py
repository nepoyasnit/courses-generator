def output_generating(model, tokenizer, prompt):
    messages = [
        {"role": "system", "content": "You are a helpful course generator. Your task is to generate courses, modules, lessons and quizes descriptions to teach user something new."},
        {"role": "user", "content": prompt}
    ]   
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512
    )
    
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return response


def generate_course_prompt(model, tokenizer, course_title: str, course_difficulty: str, modules_amount: int):
    base_prompt = f"Generate a detailed course description for a {course_difficulty} level course on {course_title} with {modules_amount} modules."

def generate_module_prompt(module_number: int,course_title: str, module_title: str, lessons_amount):
    base_prompt = f"Generate a detailed module description for {module_number}th module with title {module_title} and with {lessons_amount} lessons in course {course_title}"

def generate_lesson_prompt(lesson_number: int, lesson_title, course_title: str, module_title: str):
    base_prompt = f"Generate a detailed {lesson_number}th lesson with {lesson_title} title in module {module_title} in course {course_title}"

def generate_quiz_prompt(course_title: str, lesson_title: str, questions_amount):
    base_prompt = f"Generate a quiz description for {lesson_title} lesson in in course {course_title} with {questions_amount} questions. You don't need to generate questions, only quiz description."

def generate_question_prompt(quiz_title: str, course_title: str, lesson_title: str):
    base_prompt = f"Generate a question description for {quiz_title} quiz in {lesson_title} lesson for course {course_title}"

def generate_answer_prompt(question: str):
    base_prompt = f"Generate an answer for question: {question}"
