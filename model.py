import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

# ── TRAIN AND SAVE MODEL ──────────────────────────

def train_model():
    # Load training data
    data_path = os.path.join(os.path.dirname(__file__), "data/training_data.csv")
    df = pd.read_csv(data_path)

    # Features and target
    X = df[["rainfall", "slope", "soil_moisture", "temperature"]]
    y = df["risk"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Check accuracy
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"✅ Model trained! Accuracy: {accuracy * 100:.1f}%")

    # Save model
    model_path = os.path.join(os.path.dirname(__file__), "disaster_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("✅ Model saved to disaster_model.pkl")
    return model

# ── LOAD MODEL ────────────────────────────────────

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "disaster_model.pkl")

    # Train if model doesn't exist yet
    if not os.path.exists(model_path):
        print("No model found — training new model...")
        return train_model()

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully")
    return model

# ── PREDICT ───────────────────────────────────────

def predict_risk(rainfall, slope, soil_moisture, temperature):
    model = load_model()

    # Create input
    input_data = pd.DataFrame([[rainfall, slope, soil_moisture, temperature]],
                               columns=["rainfall", "slope", "soil_moisture", "temperature"])

    # Predict
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0]

    risk_level = "HIGH" if prediction == 1 else "LOW"
    confidence = round(max(probability) * 100, 1)

    return {
        "risk": int(prediction),
        "risk_level": risk_level,
        "confidence": confidence,
        "details": {
            "rainfall": rainfall,
            "slope": slope,
            "soil_moisture": soil_moisture,
            "temperature": temperature
        }
    }

# Train model when file is run directly
if __name__ == "__main__":
    train_model()