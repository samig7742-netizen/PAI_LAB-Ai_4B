from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['resume']
        text = extract_text(file)

        skills_list = [
            "python", "machine learning", "data science",
            "artificial intelligence", "deep learning",
            "flask", "nlp", "opencv"
        ]

        found_skills = []
        missing_skills = []

        for skill in skills_list:
            if skill in text:
                found_skills.append(skill)
            else:
                missing_skills.append(skill)

        score = int((len(found_skills) / len(skills_list)) * 100)

        return render_template(
            "result.html",
            score=score,
            skills=found_skills,
            missing=missing_skills
        )

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
