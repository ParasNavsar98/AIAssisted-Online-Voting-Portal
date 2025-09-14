import sqlite3
from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os
import re
import pandas as pd

MODEL_PATH = r"C:\Users\DELL\OneDrive\Desktop\DataBase\agent_model.pkl"
CSV_PATH = r"C:\Users\DELL\OneDrive\Desktop\AgenticAI\users.csv"



def is_email_valid(email):
    print("DEBUG: validating", email)  # debug to confirm function is running

    # Regex for basic structure: local part + domain
    pattern = r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$'
    if not re.fullmatch(pattern, email):
        return False

    # Forbidden characters anywhere
    forbidden_chars = set('$%^&*(),')
    if any(c in forbidden_chars for c in email):
        return False

    # Only one '@' allowed
    if email.count('@') != 1:
        return False

    return True






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
# Train the model from DB
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
# Load dataset emails (whitelist)
# ----------------------------
def load_dataset_emails(csv_path=CSV_PATH):
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        return set(df['email'].astype(str))
    return set()

# ----------------------------
# Rule-based + Isolation Forest verification
# ----------------------------
COMMON_WEAK_PASSWORDS = {
    "12345", "123456", "password", "admin", "qwerty", "111111"
}



def verify_user(email, password, model, dataset_emails=None):
    # 1️⃣ Allow login if user exists in dataset
    if dataset_emails and email in dataset_emails:
        return True

    # 2️⃣ Rule-based checks for unknown users
    if not is_email_valid(email):
        return False
    if password in COMMON_WEAK_PASSWORDS:
        return False

    # 3️⃣ Isolation Forest for anomaly detection
    if model is None:
        return True
    X_test = np.array([extract_features(email, password)])
    pred = model.predict(X_test)  # -1 = anomaly, 1 = normal
    return pred[0] == 1






















# import sqlite3
# from sklearn.ensemble import IsolationForest
# import numpy as np
# import joblib
# import os
# import re

# MODEL_PATH = r"C:\Users\DELL\OneDrive\Desktop\DataBase\agent_model.pkl"

# # ----------------------------
# # Feature extraction
# # ----------------------------
# def extract_features(email, password):
#     email = str(email)
#     password = str(password)

#     # Email features
#     email_len = len(email)
#     domain = email.split("@")[-1] if "@" in email else "unknown"
#     domain_encoded = hash(domain) % 100
#     at_count = email.count("@")
#     dot_count = email.count(".")

#     # Password features
#     pwd_len = len(password)
#     digits = sum(c.isdigit() for c in password)
#     specials = sum(not c.isalnum() for c in password)
#     upper = sum(c.isupper() for c in password)
#     lower = sum(c.islower() for c in password)

#     # Feature vector
#     return [email_len, pwd_len, digits, specials, upper, lower, domain_encoded, at_count, dot_count]

# # ----------------------------
# # Train the model from DB or CSV
# # ----------------------------
# def train_agent_from_db():
#     conn = sqlite3.connect(r"C:\Users\DELL\OneDrive\Desktop\DataBase\vote.db")
#     curs = conn.cursor()
#     curs.execute("SELECT email, password FROM votes")
#     data = curs.fetchall()
#     conn.close()

#     if len(data) < 5:
#         print("❌ Not enough users to train AI Agent.")
#         return None
    
#     # Convert to feature vectors
#     X = np.array([extract_features(email, password) for email, password in data])
    
#     model = IsolationForest(contamination=0.1, random_state=42)
#     model.fit(X)

#     joblib.dump(model, MODEL_PATH)
#     print(f"✅ Model trained and saved at {MODEL_PATH}")
#     return model

# # ----------------------------
# # Load model for Flask
# # ----------------------------
# def load_agent():
#     if os.path.exists(MODEL_PATH):
#         return joblib.load(MODEL_PATH)
#     return None

# # ----------------------------
# # Rule-based + Isolation Forest verification
# # ----------------------------
# COMMON_WEAK_PASSWORDS = {
#     "12345", "123456", "password", "admin", "qwerty", "111111"
# }

# def is_email_valid(email):
#     # simple check: exactly one @, at least one dot after @
#     if email.count("@") != 1:
#         return False
#     local, domain = email.split("@")
#     if "." not in domain:
#         return False
#     return True

# def verify_user(email, password, model):
#     # Rule-based checks first
#     if not is_email_valid(email):
#         return False
#     if password in COMMON_WEAK_PASSWORDS:
#         return False

#     # Use Isolation Forest for statistical anomalies
#     if model is None:
#         return True
#     X_test = np.array([extract_features(email, password)])
#     pred = model.predict(X_test)  # -1 = anomaly, 1 = normal
#     return pred[0] == 1





































# import sqlite3
# from sklearn.ensemble import IsolationForest
# import numpy as np
# import joblib
# import os

# MODEL_PATH = r"C:\Users\DELL\OneDrive\Desktop\DataBase\agent_model.pkl"

# # ----------------------------
# # Train the model from DB (run only when you want to update it)
# # ----------------------------
# def train_agent_from_db():
#     conn = sqlite3.connect(r"C:\Users\DELL\OneDrive\Desktop\DataBase\vote.db")
#     curs = conn.cursor()
#     curs.execute("SELECT LENGTH(email), LENGTH(password) FROM votes")
#     data = curs.fetchall()
#     conn.close()

#     if len(data) < 5:  # Not enough data to train
#         print("❌ Not enough users to train AI Agent.")
#         return None
    
#     X = np.array(data)
#     model = IsolationForest(contamination=0.1, random_state=42)
#     model.fit(X)

#     # Save model
#     joblib.dump(model, MODEL_PATH)
#     print(f"✅ Model trained and saved at {MODEL_PATH}")
#     return model

# # ----------------------------
# # Load model for use in Flask
# # ----------------------------
# def load_agent():
#     if os.path.exists(MODEL_PATH):
#         return joblib.load(MODEL_PATH)
#     return None

# # ----------------------------
# # Verify user at login
# # ----------------------------
# def verify_user(email, password, model):
#     if model is None:
#         return True  # allow login if model not ready
#     X_test = np.array([[len(email), len(password)]])
#     pred = model.predict(X_test)  # -1 = anomaly, 1 = normal
#     return pred[0] == 1


































# import sqlite3
# from sklearn.ensemble import IsolationForest
# import numpy as np

# def train_agent():
#     conn = sqlite3.connect(r"C:\Users\DELL\OneDrive\Desktop\DataBase\vote.db")  # same DB as your users
#     curs = conn.cursor()
#     curs.execute("SELECT LENGTH(email), LENGTH(password) FROM votes")
#     data = curs.fetchall()
    
#     if len(data) < 5:  # Not enough data to train
#         return None
    
#     X = np.array(data)
#     model = IsolationForest(contamination=0.1, random_state=42)
#     model.fit(X)
#     return model

# def verify_user(email, password, model):
#     if model is None:
#         return True  # allow login if model not ready
#     X_test = np.array([[len(email), len(password)]])
#     pred = model.predict(X_test)  # -1 = anomaly, 1 = normal
#     return pred[0] == 1



