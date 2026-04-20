import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from tensorflow.keras.models import load_model
from db import ensure_tables, create_user, get_user_by_username
from report_generator import generate_pdf_report
from news_fetcher import get_deepfake_news
import requests


# ---- Flask setup ----
app = Flask(__name__)
app.secret_key = "supersecretkey"   # TODO: use env variable
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---- Load trained deepfake model ----
MODEL_PATH = "models/deepfakess_detector_cnn_lstm.h5"
try:
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
    print(f"Model input shape: {model.input_shape}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None



# ---- Video Preprocessing ----
def preprocess_video(video_path, frame_size=(224, 224), max_frames=30):
    """Extract frames, resize, normalize, and stack into numpy array."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video info: {total_frames} frames, {fps} FPS")

    while cap.isOpened() and count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, frame_size)
        frame = frame / 255.0
        frames.append(frame)
        count += 1

    cap.release()

    if not frames:
        return None

    # Expand dims → shape: (1, T, H, W, C)
    return np.expand_dims(np.array(frames), axis=0)

# ---- Allowed file types ----
ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---- Routes ----
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)
        if user and check_password_hash(user["password"], password):
            session["user"] = username
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_pw = generate_password_hash(password)

        if get_user_by_username(username):
            flash("Username already exists", "warning")
        else:
            create_user(username, hashed_pw)
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    result, confidence, filename, pdf_path = None, None, None, None

    if request.method == "POST":
        if "video" not in request.files:
            flash("No video uploaded!", "danger")
            return redirect(request.url)

        video = request.files["video"]
        if video.filename == "":
            flash("No selected file!", "danger")
            return redirect(request.url)

        if not allowed_file(video.filename):
            flash("Invalid file type. Please upload a video.", "danger")
            return redirect(request.url)

        filename = secure_filename(video.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        video.save(filepath)
        
        print(f"Processing video: {filename}")

        if model is None:
            flash("Model not available. Please contact administrator.", "danger")
            return render_template("home.html", result=None, confidence=None, filename=None)

        frames = preprocess_video(filepath)
        if frames is None:
            flash("Error processing video.", "danger")
            return redirect(request.url)

        print(f"Input shape to model: {frames.shape}")
        prediction = model.predict(frames)[0][0]
        confidence = float(prediction)
        
        print(f"Raw prediction: {prediction}, Confidence: {confidence}")

        result = "Deepfake" if confidence >= 0.5 else "Real"
        print(f"Final result: {result}")

        # Generate report
        confidence_over_frames = [confidence] * frames.shape[1]
        pdf_path = generate_pdf_report(session["user"], filename, result, confidence, confidence_over_frames)

    return render_template("home.html", result=result, confidence=confidence, filename=filename, pdf_path=pdf_path)

@app.route("/articles")
def articles():
    if "user" not in session:
        return redirect(url_for("login"))
    news = get_deepfake_news()
    return render_template("articles.html", articles=news)




@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        user_message = request.form.get("message")
        if not user_message:
            return jsonify({"response": "Please type a message."})

        try:
            # Send user message to chatbot microservice
            response = requests.post("http://127.0.0.1:5001/chat", json={"message": user_message})
            reply = response.json().get("response", "No response received.")

            # ✅ Clean & format Markdown-like text from Gemini
            reply = (
                reply.replace("**", "<b>")
                     .replace("###", "<br><b>")
                     .replace("* ", "• ")
                     .replace("\n", "<br>")
            )

        except Exception as e:
            print("Chatbot connection error:", e)
            reply = "Chatbot service unavailable."

        return jsonify({"response": reply})

    return render_template("chatbot.html")


@app.route("/image_detect")
def image_detect():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("image_detect.html")




@app.route("/download_report")
def download_report():
    path = request.args.get("path")
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True)
    flash("Report not found.", "danger")
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    ensure_tables()
    app.run(debug=True)
