import time
import datetime
from flask import Flask, request, render_template_string
#from openai import OpenAI
from configuration import api_key, assistant_id, Models
from llama_cpp import Llama

llm = Llama(model_path="/Users/slawekpiela/Downloads/mistral-7b-v0.1.Q3_K_M.gguf")#, chat_format="llama-2")

app = Flask(__name__)
#client = OpenAI(api_key=api_key)


def query_model(prompt):
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are an assistant who pulls from files."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    # Record the time when the question is sent
    question_time = datetime.datetime.now()


    full_result = response
    result = response['choices'][0]['message']['content']


    completion_time = datetime.datetime.now()
    response_time = datetime.datetime.now()

    # Format and write log entry
    new_log_entry = (

        f"Time: {question_time}\n"
        
        f"Response Time: {response_time}\n"
        f"Question: {prompt}\n"
        f"Response: {response}\n"
        f"Full Response: {full_result}\n\n"
    )

    try:
        with open('inference_llama_log.txt', 'r+') as log_file:
            current_contents = log_file.read()
            log_file.seek(0, 0)
            log_file.write(new_log_entry + current_contents)
    except FileNotFoundError:
        with open('inference_log.txt', 'w') as log_file:
            log_file.write(new_log_entry)

    return result, response_time

def read_log_file():
    try:
        with open('inference_log.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "Log file not found."

@app.route('/', methods=['GET', 'POST'])
def index():
    response = response_time = log_contents = ""
    if request.method == 'POST' and request.form['input_text'].strip():
        input_text = request.form['input_text']
        response, response_time = query_model(input_text)
    log_contents = read_log_file()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    background-color: black;
                    color: lime;
                    font-family: Courier, monospace;
                }
                input[type="text"], input[type="submit"] {
                    background-color: #333;
                    color: lime;
                    border: 1px solid lightgrey;
                }
                .info {
                    color: lime;
                    font-family: Courier, monospace;
                    margin-bottom: 10px;
                }
                .log-contents {
                    white-space: pre-wrap;
                    color: lime;
                }
            </style>
        </head>
        <body>
            <div class="info">
                <p>Model: Llama2-7b</p>
                <p>Files: no filesK</p>
            </div>
            <form method="POST">
                <input type="text" name="input_text" size="50" value="{{ request.form.input_text }}"><br><br>
                <input type="submit" value="Submit">
            </form>
            <p>Question:</p>
            <p>{{ request.form.input_text }}</p>
            <p>Response:</p>
            <p>{{ response }}</p>
            {% if response_time %}
                <p>Response Time: {{ response_time }}</p>
            {% endif %}
            ----------------------------------------------------------------------
            <h2>Log File Contents:</h2>
            <div class="log-contents"><font size=2>{{ log_contents }}</font></div>
        </body>
        </html>
    ''', response=response, response_time=response_time, Models=Models, log_contents=log_contents)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5070,debug=True)
