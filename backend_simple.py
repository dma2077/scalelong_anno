from flask import Flask, request, jsonify
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from frontend_statistic import statistic_html

app = Flask(__name__)

# Helper function to read converted JSONL file
def read_jsonl_file(filepath, start_line=None, end_line=None):
    """Read converted JSONL file and return questions with line numbers"""
    questions_with_lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                if line.strip():
                    data = json.loads(line.strip())
                    for video_key, questions in data.items():
                        for question in questions:
                            question_with_meta = {
                                'line_number': line_num,
                                'video_key': video_key,
                                **question
                            }
                            questions_with_lines.append(question_with_meta)
        
        # Filter by line range if specified
        if start_line is not None and end_line is not None:
            questions_with_lines = [q for q in questions_with_lines 
                                  if start_line <= q['line_number'] <= end_line]
        
        return questions_with_lines
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Helper function to update correct answer
def update_correct_answer(filepath, line_number, video_key, data_id, new_answer_choice):
    """Update correct answer choice (A/B/C/D) in JSONL file"""
    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        if line_number <= len(lines):
            line_data = json.loads(lines[line_number - 1].strip())
            
            if video_key in line_data:
                for question in line_data[video_key]:
                    if question['data_id'] == data_id:
                        if new_answer_choice in ['A', 'B', 'C', 'D']:
                            question['answer'] = new_answer_choice
                            break
            
            lines[line_number - 1] = json.dumps(line_data, ensure_ascii=False) + '\n'
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            
            return True
    except Exception as e:
        print(f"Error updating JSONL file: {e}")
        return False

# Main page
@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Question Annotation Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .range-selector {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
            border: 1px solid #dee2e6;
        }
        .form-row {
            display: flex;
            gap: 20px;
            align-items: end;
        }
        .form-group {
            flex: 1;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #495057;
        }
        input, button {
            padding: 10px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14px;
        }
        .load-btn {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            padding: 10px 20px;
        }
        .load-btn:hover {
            background-color: #0056b3;
        }
        .stats-btn {
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
            margin-left: 10px;
        }
        .stats-btn:hover {
            background-color: #218838;
            text-decoration: none;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Question Annotation Tool</h1>
            <p>Select correct answers for multiple choice questions</p>
        </div>
        
        <div class="range-selector">
            <h3>Select Question Range</h3>
            <form action="/annotate" method="GET">
                <div class="form-row">
                    <div class="form-group">
                        <label for="start_line">Start Line:</label>
                        <input type="number" id="start_line" name="start_line" min="1" value="1" required>
                    </div>
                    <div class="form-group">
                        <label for="end_line">End Line:</label>
                        <input type="number" id="end_line" name="end_line" min="1" value="10" required>
                    </div>
                    <div class="form-group">
                        <button type="submit" class="load-btn">Load Questions</button>
                        <a href="/check_statistic" class="stats-btn">View Statistics</a>
                    </div>
                </div>
            </form>
        </div>
        
        <div style="text-align: center; color: #6c757d;">
            <p>Please select a line range and click "Load Questions" to start annotation.</p>
        </div>
    </div>
</body>
</html>
'''

# Annotation page
@app.route('/annotate')
def annotate():
    start_line = int(request.args.get('start_line', 1))
    end_line = int(request.args.get('end_line', 10))
    
    questions = read_jsonl_file('questions_converted.jsonl', start_line, end_line)
    
    if not questions:
        return '''
        <div style="text-align: center; padding: 50px; font-family: Arial;">
            <h2>❌ No questions found</h2>
            <p>Please check if questions_converted.jsonl exists in the current directory.</p>
            <a href="/" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">← Back</a>
        </div>
        '''
    
    # Generate HTML for questions
    questions_html = ""
    for i, question in enumerate(questions):
        options = question.get('options', {})
        current_answer = question.get('answer', 'A')
        
        # Generate options HTML
        options_html = ""
        for choice in ['A', 'B', 'C', 'D']:
            option_text = options.get(choice, f'Option {choice}')
            is_current = (choice == current_answer)
            options_html += f'''
            <div style="padding: 10px; margin: 8px 0; background-color: {'#d4edda' if is_current else '#f8f9fa'}; 
                        border-radius: 4px; border-left: 4px solid {'#28a745' if is_current else '#007bff'};">
                <strong>{choice}:</strong> {option_text}
                {' ✅ (Current)' if is_current else ''}
            </div>
            '''
        
        questions_html += f'''
        <div style="border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin-bottom: 20px; background-color: white;">
            <div style="background-color: #e9ecef; padding: 10px; border-radius: 4px; margin-bottom: 15px; font-weight: bold;">
                📋 Question {i+1} (Line {question['line_number']}, Video: {question['video_key']}, ID: {question['data_id']})
            </div>
            
                         <div style="margin-bottom: 15px; font-size: 14px; color: #6c757d;">
                 <strong>Type:</strong> {question.get('question_type', 'N/A')}
             </div>
            
                         <div style="margin-bottom: 20px;">
                 <strong>❓ Question:</strong> {question.get('question', '')}
             </div>
             
             <div style="margin-bottom: 20px;">
                 <strong>🎥 Video:</strong> 
                 <a href="https://www.youtube.com/watch?v={question['video_key']}" target="_blank" 
                    style="color: #dc3545; text-decoration: none; font-weight: bold;">
                    📺 Watch Video ({question['video_key']})
                 </a>
             </div>
            
            <div style="margin-bottom: 20px;">
                <strong>📝 Options:</strong>
                {options_html}
            </div>
            
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 4px; border: 1px solid #ffeaa7;">
                <strong>Select Correct Answer:</strong>
                <form onsubmit="updateAnswer(event, {question['line_number']}, '{question['video_key']}', {question['data_id']})" style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
                    <select name="correct_choice" required style="padding: 8px; border: 1px solid #ced4da; border-radius: 4px;">
                        <option value="A" {'selected' if current_answer == 'A' else ''}>A</option>
                        <option value="B" {'selected' if current_answer == 'B' else ''}>B</option>
                        <option value="C" {'selected' if current_answer == 'C' else ''}>C</option>
                        <option value="D" {'selected' if current_answer == 'D' else ''}>D</option>
                    </select>
                    <button type="submit" style="background-color: #28a745; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">
                        💾 Save
                    </button>
                </form>
            </div>
        </div>
        '''
    
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Question Annotation Tool</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .back-btn {{
            background-color: #6c757d;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
            margin-right: 10px;
        }}
        .back-btn:hover {{
            background-color: #5a6268;
            text-decoration: none;
            color: white;
        }}
        .stats-btn {{
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
        }}
        .stats-btn:hover {{
            background-color: #218838;
            text-decoration: none;
            color: white;
        }}
        .success-message {{
            background-color: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
            display: none;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Question Annotation</h1>
            <p>Editing questions from lines {start_line} to {end_line} ({len(questions)} questions)</p>
            <a href="/" class="back-btn">← Back</a>
            <a href="/check_statistic" class="stats-btn">📊 Statistics</a>
        </div>
        
        <div id="success-message" class="success-message"></div>
        
        {questions_html}
    </div>
    
    <script>
        function updateAnswer(event, lineNumber, videoKey, dataId) {{
            event.preventDefault();
            
            const form = event.target;
            const correctChoice = form.correct_choice.value;
            
            fetch('/update_answer', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{
                    line_number: lineNumber,
                    video_key: videoKey,
                    data_id: dataId,
                    correct_choice: correctChoice
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                const successMessage = document.getElementById('success-message');
                if (data.success) {{
                    successMessage.textContent = '✅ Answer updated successfully!';
                    successMessage.style.display = 'block';
                    successMessage.style.backgroundColor = '#d4edda';
                    successMessage.style.color = '#155724';
                    
                    // Reload page to show updated answer
                    setTimeout(() => {{
                        location.reload();
                    }}, 1000);
                }} else {{
                    successMessage.textContent = '❌ Error: ' + data.error;
                    successMessage.style.display = 'block';
                    successMessage.style.backgroundColor = '#f8d7da';
                    successMessage.style.color = '#721c24';
                }}
                
                setTimeout(() => {{
                    successMessage.style.display = 'none';
                }}, 3000);
            }})
            .catch(error => {{
                console.error('Error:', error);
                const successMessage = document.getElementById('success-message');
                successMessage.textContent = '❌ Network error';
                successMessage.style.display = 'block';
                successMessage.style.backgroundColor = '#f8d7da';
                successMessage.style.color = '#721c24';
            }});
        }}
    </script>
</body>
</html>
'''

# Update answer endpoint
@app.route('/update_answer', methods=['POST'])
def update_answer():
    data = request.get_json()
    
    success = update_correct_answer(
        'questions_converted.jsonl',
        data['line_number'],
        data['video_key'],
        data['data_id'],
        data['correct_choice']
    )
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to update file'})

# Statistics page
@app.route('/check_statistic')
def check_statistic():
    all_questions = read_jsonl_file('questions_converted.jsonl')
    
    if not all_questions:
        return "<h2>No data found. Please check if questions_converted.jsonl exists.</h2>"
    
    # Prepare data for statistics
    questions = []
    for q in all_questions:
        question_data = {
            "video_type": "sport",
            "hierarchy": "multiple_choice",  # Since granularity field is removed
            "question_type": q.get("question_type", "Unknown"),
            "wrong_choice_design": "multiple_choice"
        }
        questions.append(question_data)

    # Generate statistics
    import matplotlib
    matplotlib.use('Agg')

    # Video Type Statistics
    video_type_counts = {}
    for question in questions:
        video_type = question.get("video_type", "Unknown")
        video_type_counts[video_type] = video_type_counts.get(video_type, 0) + 1

    plt.figure(figsize=(8, 6))
    plt.bar(video_type_counts.keys(), video_type_counts.values(), color='skyblue')
    plt.title("Video Types Distribution")
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
    plt.title("Granularity Distribution")
    plt.xlabel("Granularity")
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

    plt.figure(figsize=(10, 6))
    plt.bar(question_type_counts.keys(), question_type_counts.values(), color='lightblue')
    plt.title("Question Types Distribution")
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

    # Simple design type
    wrong_choice_design_counts = {"multiple_choice": len(questions)}

    plt.figure(figsize=(8, 6))
    plt.bar(wrong_choice_design_counts.keys(), wrong_choice_design_counts.values(), color='orange')
    plt.title("Question Format")
    plt.xlabel("Format Type")
    plt.ylabel("Count")
    plt.tight_layout()

    wrong_choice_design_buf = BytesIO()
    plt.savefig(wrong_choice_design_buf, format='png')
    wrong_choice_design_buf.seek(0)
    wrong_choice_design_image_base64 = base64.b64encode(wrong_choice_design_buf.read()).decode('utf-8')
    wrong_choice_design_buf.close()
    plt.close()

    return statistic_html.format(
        video_image=video_image_base64, 
        hierarchy_image=hierarchy_image_base64, 
        question_type_image=question_type_image_base64, 
        wrong_choice_design_image=wrong_choice_design_image_base64
    )

if __name__ == '__main__':
    app.run(debug=True) 