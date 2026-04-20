# DeepFake-detection
TruthNet is an AI-based deepfake detection system using a hybrid CNN-LSTM model to analyze spatial and temporal features. It supports image/video upload, real-time detection, confidence scores, and report generation via a web-based interface.
🔍 TruthNet – AI-Powered Deepfake Detection

TruthNet is a hybrid CNN-LSTM based deepfake detection system that analyzes both spatial and temporal features to identify manipulated images and videos through a web-based interface.

🚀 Features
Deepfake detection for images & videos
Hybrid CNN + LSTM model (spatio-temporal analysis)
Real-time prediction with confidence score
User authentication system
PDF report generation
News API integration (AI/deepfake updates)
Simple web interface
🧠 Project Structure
TruthNet/
│── __pycache__/
│── chatbot_env/          # Chatbot environment (optional module)
│── deepfake_env/         # Deepfake model environment
│── models/               # Trained ML models (.h5 etc.)
│── static/               # CSS, JS, assets
│── templates/            # HTML files (UI)
│── uploads/              # Uploaded media files
│
│── app.py                # Main Flask app
│── chatbot_service.py    # Chatbot integration
│── db.py                 # Database handling
│── news_fetcher.py       # News API integration
│── report_generator.py   # PDF report generation
│── requirements.txt      # Dependencies
│── users.db              # SQLite/PostgreSQL DB
⚙️ Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Flask (Python)
Database: PostgreSQL / SQLite
ML: TensorFlow, OpenCV, NumPy, Pandas
Other: ReportLab, Matplotlib, News API
▶️ How to Run
# Clone repo
git clone https://github.com/your-username/truthnet.git
cd truthnet

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
🔄 Workflow

Upload → Preprocessing → CNN (features) → LSTM (sequence) → Prediction → Result + Report

📊 Performance
Accuracy: ~80%
Strong fake detection recall (~0.94)
Robust on high-quality deepfakes
