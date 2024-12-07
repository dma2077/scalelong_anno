statistic_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Statistics</title>
</head>
<body>
    <h1>Video Type Statistics</h1>
    <div>
        <img src="data:image/png;base64,{video_image}" alt="Video Type Statistics">
    </div>
    <h1>Hierarchy Statistics</h1>
    <div>
        <img src="data:image/png;base64,{hierarchy_image}" alt="Hierarchy Statistics">
    </div>
    <h1>Question Type Statistics</h1>
    <div>
        <img src="data:image/png;base64,{question_type_image}" alt="Question Type Statistics">
    </div>
    <h1>Wrong Choice Design Statistics</h1>
    <div>
        <img src="data:image/png;base64,{wrong_choice_design_image}" alt="Wrong Choice Design Statistics">
    </div>
    <a href="/">Back to Home</a>
</body>
</html>
"""