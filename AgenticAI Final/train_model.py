import sqlite3
from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os
import re

MODEL_PATH = r"C:\Users\DELL\OneDrive\Desktop\DataBase\agent_model.pkl"

# ----------------------------
# Feature extraction
# ----------------------------
def extract_features(email, password):
    email = str(email)
    password = str(password)

    # Email features
    email_len = len(email)
    domain = email.split("@")[-1] if "@" in email else "unknown"
    domain_encoded = hash(domain) % 100
    at_count = email.count("@")
    dot_count = email.count(".")

    # Password features
    pwd_len = len(password)
    digits = sum(c.isdigit() for c in password)
    specials = sum(not c.isalnum() for c in password)
    upper = sum(c.isupper() for c in password)
    lower = sum(c.islower() for c in password)

    # Feature vector
    return [email_len, pwd_len, digits, specials, upper, lower, domain_encoded, at_count, dot_count]

# ----------------------------
# Train the model from DB or CSV
# ----------------------------
def train_agent_from_db():
    conn = sqlite3.connect(r"C:\Users\DELL\OneDrive\Desktop\DataBase\vote.db")
    curs = conn.cursor()
    curs.execute("SELECT email, password FROM votes")
    data = curs.fetchall()
    conn.close()

    if len(data) < 5:
        print("❌ Not enough users to train AI Agent.")
        return None
    
    # Convert to feature vectors
    X = np.array([extract_features(email, password) for email, password in data])
    
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)

    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model trained and saved at {MODEL_PATH}")
    return model

# ----------------------------
# Load model for Flask
# ----------------------------
def load_agent():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

# ----------------------------
# Verify user at login
# ----------------------------
def verify_user(email, password, model):
    if model is None:
        return True  # allow login if model not ready
    X_test = np.array([extract_features(email, password)])
    pred = model.predict(X_test)  # -1 = anomaly, 1 = normal
    return pred[0] == 1
