# 🛡️ Tool for Real-Time Feeds of Cyber Incident Detection

A Flask-based web application for real-time detection of cyber threats including **Phishing URLs**, **Network Anomalies**, and **Business Email Compromise (BEC)** attacks using Machine Learning models.

---

## 📌 Features

- **Phishing URL Detection** — Analyzes URLs in real-time using a Gradient Boosting Classifier with 30 extracted features
- **Network Anomaly Detection** — Detects unusual network traffic patterns using a trained anomaly detection model
- **BEC Email Detection** — Identifies Business Email Compromise attempts using Random Forest + TF-IDF vectorization

---

## 🧠 Technologies Used

| Category | Tools |
|----------|-------|
| Backend | Python, Flask |
| Machine Learning | Scikit-learn, TensorFlow/Keras |
| NLP | TF-IDF Vectorizer |
| Data Processing | Pandas, NumPy |
| Web Scraping | BeautifulSoup4, Requests |
| Domain Analysis | python-whois, python-dateutil |
| Models | Gradient Boosting, Random Forest, Isolation Forest |

---

## 📁 Project Structure

```
Intrusion Detection System/
├── app.py                  # Main Flask application
├── feature.py              # URL feature extraction (30 features)
├── phishing.csv            # Phishing dataset
├── anomoly_model.pkl       # Trained anomaly detection model
├── random_forest_model.pkl # Trained BEC detection model
├── tfidf_vectorizer.pkl    # TF-IDF vectorizer for email text
├── label_encoder.pkl       # Label encoder
├── bec1.pkl                # BEC model
├── all_data.csv            # Network traffic dataset
├── BEC_Datasets1.csv       # BEC email dataset
├── static/                 # Static files (CSS, JS, images)
└── templates/              # HTML templates
    ├── login.html
    ├── index.html
    ├── service.html
    ├── anamoly.html
    ├── bec.html
    └── about.html
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.12+
- pip

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/tool-for-realtime-cyber-incident-feeds.git
cd tool-for-realtime-cyber-incident-feeds
```

### Step 2: Install Dependencies
```bash
pip install flask
pip install tensorflow
pip install scikit-learn==1.5.0
pip install imbalanced-learn==0.12.3
pip install beautifulsoup4==4.12.2
pip install google-search==1.1.1
pip install python-whois==0.8.0
pip install python-dateutil==2.8.2
pip install pandas
pip install joblib
pip install requests
pip install numpy
pip install opencv-python
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Open in Browser
```
http://127.0.0.1:5000
```

**Login Credentials:**
- Username: `admin`
- Password: `admin`

---

## 🚀 Usage

### 1. Phishing URL Detection
- Navigate to `/prediction`
- Enter any URL
- The model returns the probability of the URL being safe or phishing

### 2. Network Anomaly Detection
- Navigate to `/predict`
- Enter network traffic parameters (packet counts, TCP/UDP metrics)
- The model classifies traffic as normal or anomalous

### 3. BEC Email Detection
- Navigate to `/becpredict`
- Enter email content/ID
- The model classifies the email as safe or a BEC attack

---

## 📊 Models & Accuracy

| Model | Algorithm | Use Case |
|-------|-----------|----------|
| Phishing Detector | Gradient Boosting + RFECV | URL Classification |
| Anomaly Detector | Isolation Forest | Network Traffic |
| BEC Detector | Random Forest + TF-IDF | Email Classification |

---

## 🔗 Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET/POST | Login page |
| `/home` | GET | Dashboard |
| `/prediction` | GET/POST | Phishing URL check |
| `/predict` | GET/POST | Network anomaly detection |
| `/becpredict` | GET/POST | BEC email detection |
| `/about` | GET | About page |
| `/logout` | GET | Logout |

---

## ⚠️ Disclaimer

This tool is developed for **educational and research purposes only**. Do not use it in production environments without proper security hardening.

---

## 📄 License

This project is for academic use only.
