main_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dataset Creator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background-color: #ffffff;
            padding: 20px 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .form-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            width: 100%;
        }

        h1 {
            color: #333;
            font-size: 1.5rem;
            margin-bottom: 20px;
            text-align: center;
        }

        label {
            color: #555;
            font-size: 0.9rem;
            margin-bottom: 5px;
            display: block;
        }

        input[type="text"], textarea, select {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 0.9rem;
        }

        textarea {
            height: 90px;
        }

        .button-container {
            display: flex;
            justify-content: space-between;
            width: 100%;
            margin-top: 20px;
        }

        button {
            padding: 10px;
            font-size: 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .save-button {
            background-color: #4CAF50;
            color: white;
        }

        .save-button:hover {
            background-color: #45a049;
        }

        .check-button {
            background-color: #f44336;
            color: white;
        }

        .check-button:hover {
            background-color: #d32f2f;
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 0.8rem;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Create a Multi-Choice Question</h1>
        <form action="/save_question" method="post" class="form-section">
            <div>
                <label for="question_title">Question Title:</label>
                <textarea id="question_title" name="question_title" placeholder="Enter your question" required></textarea>

                <label for="choice_a">Choice A:</label>
                <input type="text" id="choice_a" name="choice_a" placeholder="Enter choice A" required>

                <label for="choice_b">Choice B:</label>
                <input type="text" id="choice_b" name="choice_b" placeholder="Enter choice B" required>

                <label for="choice_c">Choice C:</label>
                <input type="text" id="choice_c" name="choice_c" placeholder="Enter choice C" required>

                <label for="choice_d">Choice D:</label>
                <input type="text" id="choice_d" name="choice_d" placeholder="Enter choice D" required>
            </div>

            <div>
                <label for="correct_answer">Correct Answer:</label>
                <select id="correct_answer" name="correct_answer" required>
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                </select>

                <label for="hierarchy">Hierarchy:</label>
                <select id="hierarchy" name="hierarchy" required>
                    <option value="clip">Clip</option>
                    <option value="shot">Shot</option>
                    <option value="event">Event</option>
                    <option value="story">Story</option>
                </select>

                <label for="time_reference">Time Reference:</label>
                <input type="text" id="time_reference" name="time_reference" placeholder="Enter time reference" required>

                <label for="video_key">Video Key:</label>
                <input type="text" id="video_key" name="video_key" placeholder="Enter video key" required>

                <label for="video_type">Video Type:</label>
                <select id="video_type" name="video_type" required>
                    <option value="tv">TV</option>
                    <option value="sport">Sport</option>
                    <option value="cartoon">Cartoon</option>
                    <option value="live">Live</option>
                    <option value="selfmedia">Self Media</option>
                    <option value="documentary">Documentary</option>
                </select>

                <label for="question_type">Question Type:</label>
                <select id="question_type" name="question_type" required>
                    <option value="Causal Reasoning">Causal Reasoning</option>
                    <option value="Objective Recognition">Objective Recognition</option>
                    <option value="Information Summary">Information Summary</option>
                    <option value="Action Understanding">Action Understanding</option>
                    <option value="Counting Problem">Counting Problem</option>
                </select>

                <label for="wrong_choice_design">Wrong Choice Design:</label>
                <select id="wrong_choice_design" name="wrong_choice_design" required>
                    <option value="visual replacement">Visual Replacement</option>
                    <option value="quantitative replacement">Quantitative Replacement</option>
                    <option value="action replacement">Action Replacement</option>
                    <option value="character replacement">Character Replacement</option>
                    <option value="spatial replacement">Spatial Replacement</option>
                    <option value="temporal replacement">Temporal Replacement</option>
                    <option value="missing information">Missing Information</option>
                    <option value="detail replacement">Detail Replacement</option>
                    <option value="sequential replacement">Sequential Replacement</option>
                    <option value="frequency replacement">Frequency Replacement</option>
                </select>
            </div>

            <div class="button-container">
                <button type="submit" class="save-button">Save Question</button>
                <button type="button" class="check-button" onclick="window.location.href='/check_statistic'">Check Statistic</button>
            </div>
        </form>
        <div class="footer">
            &copy; 2024 Dataset Creator
        </div>
    </div>
</body>
</html>
'''