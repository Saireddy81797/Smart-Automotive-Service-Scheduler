import os
import joblib

# Path where the ML model will be saved + loaded from
MODEL_PATH = os.path.join("ml", "slot_rf.pkl")


def load_model():
    """
    Loads the trained slot ranking model from disk.
    Returns None if model file does not exist (first-time run).
    """
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception as e:
            print("❌ Error loading model:", e)
            return None
    return None


def save_model(model):
    """
    Saves a trained ML model to disk.
    """
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved at: {MODEL_PATH}")
