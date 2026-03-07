import cv2
import numpy as np
from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Load YOLO model
net = cv2.dnn.readNet("model/yolov4.weights", "model/yolov4.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    count = 0
    object_ids = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        
        # Prepare frame for YOLO
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), 
                                     (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    # Count objects only in the lower half
                    if center_y > height // 2:
                        object_ids.add((x, y))  # Use coordinates as unique ID
                        count = len(object_ids)

                    # Draw bounding box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)
                    cv2.putText(frame, str(class_id), (x, y-5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        # Draw middle line
        cv2.line(frame, (0, height//2), (width, height//2), (0,0,255), 2)

        # Optional: save processed frames to video (if needed)
        # Here you can write frame to output video using VideoWriter

    cap.release()
    return count

@app.route("/", methods=["GET", "POST"])
def index():
    total_count = None
    video_name = None

    if request.method == "POST":
        video = request.files.get("video")
        if video:
            video_name = video.filename
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
            video.save(video_path)

            output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"processed_{video_name}")
            total_count = process_video(video_path, output_path)

    return render_template("index.html", count=total_count, video_name=video_name)

if __name__ == "__main__":
    app.run(debug=True)