from flask import Flask, render_template, request
import os
from resume_parser import extract_text_from_resume
from analyzer import analyze_resume
from ats_tips import get_ats_tips

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]
    job_description = request.form.get("job_description", "")

    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    resume_text = extract_text_from_resume(filepath)
    result = analyze_resume(resume_text, job_description)
    ats_tips = get_ats_tips(result["missing_keywords"])

    return render_template("result.html", result=result, ats_tips=ats_tips)

if __name__ == "__main__":
    app.run(debug=True)