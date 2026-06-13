from flask import Flask, request, jsonify, render_template
import os

from db import init_db, register_user, login_user, save_score, get_scores
from model import generate_questions, evaluate_answer
from resume_parser import extract_skills
from camera import analyze_confidence

app = Flask(__name__,
            template_folder="../templates",
            static_folder="../static")

# Upload folder
UPLOAD_FOLDER = "../uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize DB
init_db()

# -------------------- PAGES --------------------

@app.route('/')
def home():
    return render_template("login.html")


@app.route('/interview')
def interview():
    return render_template("index.html")


@app.route('/dashboard_page')
def dashboard_page():
    return render_template("dashboard.html")


# -------------------- AUTH --------------------

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    success = register_user(
        data['username'],
        data['password'],
        data.get('name', ''),
        data.get('course', '')
    )

    if success:
        return jsonify({"msg": "ok"})
    else:
        return jsonify({"msg": "exists"})


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = login_user(data['username'], data['password'])

    if user:
        return jsonify({"msg": "ok"})
    else:
        return jsonify({"msg": "fail"})


# -------------------- RESUME --------------------

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No filename"}), 400

    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    skills = extract_skills(path)

    print("Skills:", skills)

    return jsonify({"skills": skills})


# -------------------- INTERVIEW --------------------

@app.route('/questions', methods=['POST'])
def questions():
    data = request.json

    role = data.get('role', 'technical')
    skills = data.get('skills', [])

    qs = generate_questions(role, skills)

    return jsonify({"questions": qs})


@app.route('/answer', methods=['POST'])
def answer():
    data = request.json

    score, fb = evaluate_answer(data['q'], data['a'])

    save_score(data.get('username', 'user'), score)

    return jsonify({
        "score": score,
        "fb": fb
    })


# -------------------- CAMERA --------------------

@app.route('/confidence')
def confidence():

    cam = analyze_confidence()

    return {
        "confidence": cam["score"],
        "camera_feedback": cam["msg"]
    }

from voice_confidence import analyze_voice

@app.route('/voice_confidence')
def voice_confidence():

    score, msg = analyze_voice()

    return {
        "voice_score": score,
        "voice_feedback": msg
    }


# -------------------- DASHBOARD --------------------

@app.route('/dashboard')
def dashboard():
    data = get_scores()

    scores = [d[1] for d in data]

    if not scores:
        return {
            "avg": 0,
            "latest": 0,
            "highest": 0,
            "total": 0,
            "feedback": "No data available",
            "level": "Beginner",
            "scores": []
        }

    avg = sum(scores) / len(scores)
    latest = scores[-1]
    highest = max(scores)
    total = len(scores)

    # PERFORMANCE LEVEL
    if avg > 80:
        level = "Excellent"
        fb = "You are interview ready. Keep refining answers."
    elif avg > 60:
        level = "Good"
        fb = "Work on confidence and deeper explanations."
    else:
        level = "Needs Improvement"
        fb = "Practice basics, communication, and clarity."

    return {
        "avg": avg,
        "latest": latest,
        "highest": highest,
        "total": total,
        "level": level,
        "feedback": fb,
        "scores": scores
    }




# -------------------- RUN --------------------

if __name__ == "__main__":
    app.run(debug=True)
