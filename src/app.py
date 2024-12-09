import sqlite3
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.registration import register_user, login_user, USER_EMAIL, USER_PASSWORD

# model_name = "Qwen/Qwen2.5-0.5B-Instruct"

# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     torch_dtype="auto",
#     device_map="auto",
#     token="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"
# )
# tokenizer = AutoTokenizer.from_pretrained(model_name)


def generate_course(topic, difficulty):
    """
    Generate a course outline based on the given topic and difficulty level.
    """
    prompt = f"Generate a detailed course outline for a {difficulty} level course on {topic}. Include modules, topics covered, and expected outcomes."
    messages = [
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
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
            fn=login_user, 
            inputs=[login_email, login_password], 
            outputs=authorization_area)
        
        register_button.click(
            fn=register_user, 
            inputs=[register_username, register_email, register_password], 
            outputs=authorization_area)


    with gr.Tab("LLM Auto-Suggestions"):
        gr.Markdown("# 📚 Course Outline Generator")
        
        with gr.Row():
            topic_input = gr.Textbox(label="Course Topic", placeholder="e.g., Machine Learning, Art History")
            difficulty_dropdown = gr.Dropdown(choices=["beginner", "intermediate", "advanced"], label="Difficulty Level")
            modules_amount = gr.Number("Number of modules in course", minimum=1, maximum=10, step=1)
        
        generate_button = gr.Button("Generate Course")
        
        output_area = gr.Textbox(label="Generated Course Outline", lines=20, placeholder="Your course outline will appear here.")
        
        generate_button.click(
            fn=generate_course, 
            inputs=[topic_input, difficulty_dropdown], 
            outputs=output_area)

# Launch the app
app.launch()
