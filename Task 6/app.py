import cv2
import mediapipe as mp
import numpy as np
import os
import base64
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
NOSE_TIP = 1
MOUTH = [61, 291]
JAWLINE = [234, 454] 
def get_distance(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
def analyze_face(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None, "Invalid image"
    h, w, _ = img.shape
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_img)
    if not results.multi_face_landmarks:
        return None, "No face detected"
    landmarks = results.multi_face_landmarks[0].landmark
    eye_dist = get_distance(landmarks[LEFT_EYE[0]], landmarks[RIGHT_EYE[0]])
    jaw_width = get_distance(landmarks[JAWLINE[0]], landmarks[JAWLINE[1]])
    mouth_width = get_distance(landmarks[MOUTH[0]], landmarks[MOUTH[1]])
    nose_length = get_distance(landmarks[NOSE_TIP], landmarks[168]) 
    eye_ratio = eye_dist / jaw_width
    mouth_ratio = mouth_width / jaw_width
    nose_ratio = nose_length / jaw_width
    p_type = ""
    p_type += "E" if eye_ratio > 0.45 else "I"
    p_type += "N" if nose_ratio > 0.25 else "S"
    p_type += "F" if mouth_ratio > 0.35 else "T"
    p_type += "P" if (eye_ratio + mouth_ratio) > 0.8 else "J"
    descriptions = {
        "ISTJ": "Practical and fact-minded, whose reliability cannot be doubted.",
        "ENFP": "Enthusiastic, creative and sociable free spirits, who can always find a reason to smile.",
        "INTJ": "Imaginative and strategic thinkers, with a plan for everything.",
        "ENTP": "Smart and curious thinkers who cannot resist an intellectual challenge.",
        "INFJ": "Quiet and mystical, yet very inspiring and tireless idealists.",
        "ENFJ": "Charismatic and inspiring leaders, able to mesmerize their listeners.",
        "INFP": "Poetic, kind and altruistic people, always eager to help a good cause.",
        "ESFJ": "Extraordinarily caring, social and popular people, always eager to help.",
        "ESTJ": "Excellent administrators, unsurpassed at managing things – or people.",
        "ISTP": "Bold and practical experimenters, masters of all kinds of tools.",
        "ESTP": "Smart, energetic and very perceptive people, who truly enjoy living on the edge.",
        "INTP": "Innovative inventors with an unquenchable thirst for knowledge.",
        "ISFJ": "Very dedicated and warm protectors, always ready to defend their loved ones.",
        "ESFP": "Spontaneous, energetic and enthusiastic people – life is never boring around them.",
        "ISFP": "Flexible and charming artists, always ready to explore and experience something new.",
        "ENTJ": "Bold, imaginative and strong-willed leaders, always finding a way – or making one."
    }
    result_data = {
        "type": p_type,
        "description": descriptions.get(p_type, "Unique personality profile."),
        "measurements": {
            "Eye Gap Ratio": f"{eye_ratio:.2f}",
            "Mouth Width Ratio": f"{mouth_ratio:.2f}",
            "Nose Length Ratio": f"{nose_ratio:.2f}",
            "Face Breadth": f"{jaw_width:.2f}"
        }
    }
    for lm in landmarks:
        cv2.circle(img, (int(lm.x * w), int(lm.y * h)), 1, (0, 255, 0), -1)
    processed_filename = "processed_" + os.path.basename(image_path)
    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
    cv2.imwrite(processed_path, img)
    return result_data, processed_path
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            return render_template("index.html", error="No file uploaded")
        file = request.files['file']
        if file.filename == '':
            return render_template("index.html", error="No file selected")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        result, processed_img = analyze_face(filepath)
        if result is None:
            return render_template("index.html", error=processed_img)
        return render_template("index.html", result=result, image=processed_img)
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True, port=5001)