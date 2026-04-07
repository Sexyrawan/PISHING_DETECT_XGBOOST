# 🛡️ PhishGuard — AI-Powered Phishing URL Detector

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-FF6F00?style=for-the-badge&logo=xgboost&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Scan any URL instantly and detect phishing attempts using Machine Learning.**

[Live Demo](#-live-demo) · [Features](#-features) · [Tech Stack](#-tech-stack) · [Setup](#-local-setup) · [API](#-api-endpoints)

</div>

---

## 🎯 What is PhishGuard?

PhishGuard is a web application that uses an **XGBoost machine learning model** to detect phishing URLs in real-time. Simply paste any suspicious URL, and the model analyzes **48 URL-based features** to determine whether it's a phishing attempt or a legitimate website — with **98.6% accuracy**.

> 🔒 No data is sent to external services. The ML model runs entirely on the server.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Instant URL Scanning** | Paste any URL and get results in milliseconds |
| 🤖 **XGBoost ML Model** | Trained on 10,000+ phishing & legitimate URLs |
| 📊 **Confidence Score** | See how confident the model is about its prediction |
| 🧠 **48 Feature Analysis** | Examines URL structure, domain patterns, and suspicious indicators |
| 📜 **Scan History** | View all previously scanned URLs with timestamps |
| 🌐 **REST API** | JSON API endpoint for programmatic access |
| 🎨 **Modern Dark UI** | Neumorphic design with smooth animations |

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────┐
│              PhishGuard Stack               │
├─────────────┬───────────────────────────────┤
│  Frontend   │  HTML5 · CSS3 · Jinja2        │
│  Backend    │  FastAPI · Uvicorn             │
│  ML Model   │  XGBoost · scikit-learn        │
│  Database   │  SQLite · SQLAlchemy           │
│  Validation │  Pydantic                      │
│  Hosting    │  Render (Free Tier)            │
└─────────────┴───────────────────────────────┘
```

---

## 🚀 Live Demo

> **🌐 [https://phishguard.onrender.com](https://phishguard.onrender.com)**
>
> *Note: Free tier may take ~30s to wake up on first visit.*

---

## 📁 Project Structure

```
PISHING_DETECT_XGBOOST/
├── main.py                    # FastAPI app entry point
├── requirements.txt           # Python dependencies
├── Procfile                   # Render deployment command
├── render.yaml                # Render Blueprint config
│
├── model/
│   ├── pridect.py             # Feature extraction & prediction logic
│   ├── train_model.py         # One-time model training script
│   ├── xgb_phishing_model.pkl # Trained XGBoost model
│   └── feature_names.pkl      # Feature column names
│
├── routes/
│   └── pridect.py             # API & page route handlers
│
├── database/
│   ├── db.py                  # SQLAlchemy engine & session setup
│   └── models.py              # ScanResult ORM model
│
├── schemas/
│   └── pishing.py             # Pydantic request/response schemas
│
├── tampletes/
│   ├── index.html             # Homepage with scan form
│   ├── result.html            # Scan result page
│   └── history.html           # Scan history page
│
└── static/
    └── style.css              # Dark neumorphic styling
```

---

## 💻 Local Setup

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Sexyrawan/PISHING_DETECT_XGBOOST.git
cd PISHING_DETECT_XGBOOST

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
uvicorn main:app --reload
```

Open **http://localhost:8000** in your browser. 🎉

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Homepage with URL scan form |
| `POST` | `/scan` | Scan a URL (form data: `url`) |
| `GET` | `/history` | View all past scan results |
| `GET` | `/api/history` | JSON API — all scan results |

### Example API Usage

```bash
# Get scan history as JSON
curl https://phishguard.onrender.com/api/history
```

---

## 🧠 How It Works

```
User enters URL
       │
       ▼
┌──────────────────┐
│ Feature Extractor │ → Parses 48 numeric features from URL
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  XGBoost Model   │ → Binary classification (Phishing / Legitimate)
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Result + Score  │ → Confidence percentage + save to database
└──────────────────┘
```

### Features Analyzed (48 total)
- **URL Structure**: length, dots, dashes, underscores, special characters
- **Domain Patterns**: subdomain levels, IP address usage, HTTPS presence
- **Suspicious Indicators**: sensitive words (login, verify, account, etc.)
- **Path Analysis**: path depth, query parameters, double slashes
- **Security Signals**: at-symbol usage, tilde, numeric character ratio

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| **Accuracy** | 98.6% |
| **Algorithm** | XGBoost Classifier |
| **Training Data** | 10,000+ URLs (balanced phishing/legitimate) |
| **Features** | 48 URL-based numeric features |
| **Train/Test Split** | 80/20 stratified |

---

## 🤝 Contributors

- **Rahul Kashyap** — ML Model & Backend
- **Harsh Shrisvatav** — Frontend & Deployment

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**⭐ If you found this useful, give it a star!**

Made with ❤️ using FastAPI & XGBoost

</div>
