import webbrowser
from flask import Flask, send_from_directory, request, jsonify, render_template
import subprocess
import json
import time
import threading
import os
from jinja2 import Template

# Define a global variable for predefined_text
actual_pin = "54"
last_pin = "11"

app = Flask(__name__)


def generate_html(actual, last):
    # Read HTML template from file
    with open("index.html", "r") as file:
        html_template = file.read()
    #print("PIN", pin)
    # Replace the placeholder with the actual predefined_text value
    rendered_html_ = html_template.replace(f'const predefinedText = "{last}";', f'const predefinedText = "{actual}";')

    return rendered_html_



@app.route('/')
def index():
    global actual_pin
    global last_pin
    return generate_html(actual_pin, last_pin)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

#if __name__ == '__main__':
    #webbrowser.open('http://localhost:80')
    #print('Please access http://localhost:8000 in your web browser to download the images.')
    
def startServer():
    app.run(port=5001, debug=False)


# Example function to update predefined_text dynamically
def update_predefined_text(actual, last):
    global actual_pin
    global last_pin
    actual_pin = actual
    last_pin = last
    #predefined_text = new_text
    # Render the template
    rendered_html = generate_html(actual, last)
    #print("new_text", actual)
    # Update the existing HTML file with the rendered HTML
    with open("index.html", "w") as file:
        file.write(rendered_html)

