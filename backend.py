from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from frontend_main import main_html
from frontend_statistic import statistic_html


app = Flask(__name__)

# Route for the front-end
@app.route('/')
def home():
    return main_html

# Route for saving the question
@app.route('/save_question', methods=['POST'])
def save_question():
    question_title = request.form['question_title']
    choice_a = request.form['choice_a']
    choice_b = request.form['choice_b']
    choice_c = request.form['choice_c']
    choice_d = request.form['choice_d']
    correct_answer = request.form['correct_answer']
    hierarchy = request.form['hierarchy']
    time_reference = request.form['time_reference']
    video_key = request.form['video_key']
    video_type = request.form['video_type']
    question_type = request.form['question_type']
    wrong_choice_design = request.form['wrong_choice_design']

    question_data = {
        "title": question_title,
        "choices": {
            "A": choice_a,
            "B": choice_b,
            "C": choice_c,
            "D": choice_d
        },
        "correct_answer": correct_answer,
        "hierarchy": hierarchy,
        "time_reference": time_reference,
        "video_key": video_key,
        "video_type": video_type,
        "question_type": question_type,
        "wrong_choice_design": wrong_choice_design
    }

    # Save the question to a JSON file
    try:
        with open('questions.json', 'r') as file:
            questions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        questions = []

    questions.append(question_data)

    with open('questions.json', 'w') as file:
        json.dump(questions, file, indent=4)

    # Redirect back to the front-end to create new questions
    return redirect(url_for('home'))

# Route for checking statistics
@app.route('/check_statistic', methods=['GET'])
def check_statistic():
    try:
        with open('questions.json', 'r') as file:
            questions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        questions = []

    # Video Type Statistics
    video_type_counts = {}
    for question in questions:
        video_type = question.get("video_type", "Unknown")
        video_type_counts[video_type] = video_type_counts.get(video_type, 0) + 1

    import matplotlib
    matplotlib.use('Agg')

    # Plot Video Type Statistics
    plt.figure(figsize=(8, 6))
    plt.bar(video_type_counts.keys(), video_type_counts.values(), color='skyblue')
    plt.title("Proportion of Video Types")
    plt.xlabel("Video Type")
    plt.ylabel("Count")
    plt.tight_layout()

    video_buf = BytesIO()
    plt.savefig(video_buf, format='png')
    video_buf.seek(0)
    video_image_base64 = base64.b64encode(video_buf.read()).decode('utf-8')
    video_buf.close()
    plt.close()

    # Hierarchy Statistics
    hierarchy_counts = {}
    for question in questions:
        hierarchy = question.get("hierarchy", "Unknown")
        hierarchy_counts[hierarchy] = hierarchy_counts.get(hierarchy, 0) + 1

    plt.figure(figsize=(8, 6))
    plt.bar(hierarchy_counts.keys(), hierarchy_counts.values(), color='lightgreen')
    plt.title("Proportion of Hierarchy Types")
    plt.xlabel("Hierarchy")
    plt.ylabel("Count")
    plt.tight_layout()

    hierarchy_buf = BytesIO()
    plt.savefig(hierarchy_buf, format='png')
    hierarchy_buf.seek(0)
    hierarchy_image_base64 = base64.b64encode(hierarchy_buf.read()).decode('utf-8')
    hierarchy_buf.close()
    plt.close()

    # Question Type Statistics
    question_type_counts = {}
    for question in questions:
        question_type = question.get("question_type", "Unknown")
        question_type_counts[question_type] = question_type_counts.get(question_type, 0) + 1

    plt.figure(figsize=(8, 6))
    plt.bar(question_type_counts.keys(), question_type_counts.values(), color='lightblue')
    plt.title("Proportion of Question Types")
    plt.xlabel("Question Type")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Count")
    plt.tight_layout()

    question_type_buf = BytesIO()
    plt.savefig(question_type_buf, format='png')
    question_type_buf.seek(0)
    question_type_image_base64 = base64.b64encode(question_type_buf.read()).decode('utf-8')
    question_type_buf.close()
    plt.close()

    # Wrong Choice Design Statistics
    wrong_choice_design_counts = {}
    for question in questions:
        wrong_choice_design = question.get("wrong_choice_design", "Unknown")
        wrong_choice_design_counts[wrong_choice_design] = wrong_choice_design_counts.get(wrong_choice_design, 0) + 1

    plt.figure(figsize=(8, 6))
    plt.bar(wrong_choice_design_counts.keys(), wrong_choice_design_counts.values(), color='orange')
    plt.title("Proportion of Wrong Choice Designs")
    plt.xlabel("Wrong Choice Design")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    wrong_choice_design_buf = BytesIO()
    plt.savefig(wrong_choice_design_buf, format='png')
    wrong_choice_design_buf.seek(0)
    wrong_choice_design_image_base64 = base64.b64encode(wrong_choice_design_buf.read()).decode('utf-8')
    wrong_choice_design_buf.close()
    plt.close()

    return statistic_html.format(video_image=video_image_base64, hierarchy_image=hierarchy_image_base64, question_type_image=question_type_image_base64, wrong_choice_design_image=wrong_choice_design_image_base64)


if __name__ == '__main__':
    app.run(debug=True)
