"""
train_model.py  — One-time script to train XGBoost on the CSV dataset and save the model.

Run this once:   python -m model.train_model
"""

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# ── 1. Load Data ────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "archive", "Phishing_Legitimate_full.csv")
df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")
print(f"Phishing: {(df['CLASS_LABEL'] == 1).sum()}  |  Legitimate: {(df['CLASS_LABEL'] == 0).sum()}")

# ── 2. Separate Features & Label ────────────────────────────
# Drop 'id' (not a feature) and 'CLASS_LABEL' (target)
X = df.drop(columns=["id", "CLASS_LABEL"])
y = df["CLASS_LABEL"]

# Save feature names for later use
FEATURE_NAMES = list(X.columns)

# ── 3. Train/Test Split ─────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain set: {X_train.shape[0]} rows")
print(f"Test  set: {X_test.shape[0]} rows")

# ── 4. Train XGBoost ────────────────────────────────────────
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric="logloss",
    random_state=42,
)

model.fit(X_train, y_train)

# ── 5. Evaluate ─────────────────────────────────────────────
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\n✅ Accuracy: {acc:.4f}  ({acc*100:.2f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))

# ── 6. Save Model + Feature Names ───────────────────────────
MODEL_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(MODEL_DIR, "xgb_phishing_model.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "feature_names.pkl")

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

with open(FEATURES_PATH, "wb") as f:
    pickle.dump(FEATURE_NAMES, f)

print(f"\n💾 Model saved  → {MODEL_PATH}")
print(f"💾 Features saved → {FEATURES_PATH}")
