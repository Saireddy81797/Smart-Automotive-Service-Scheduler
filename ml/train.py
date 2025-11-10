import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from .features import make_features
from .model_store import MODEL_PATH


def train_model():
    """
    Trains a RandomForest model using synthetic slot history data.
    This is only for demo purposes. In real usage, this will learn
    from actual booking + slot utilization patterns.
    """

    # Synthetic dataset (You can replace with real data later)
    df = pd.DataFrame({
        "remaining":           [0,1,2,3,4,1,2,3,0,4,2,1,3,4,2,1],
        "service_minutes":     [60,60,60,60,60,90,90,30,30,45,120,45,60,30,60,90],
        "label":               [0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1]  # 1 = good slot, 0 = bad
    })

    X, y = make_features(df)

    clf = RandomForestClassifier(
        n_estimators=80,
        max_depth=6,
        random_state=42
    )

    clf.fit(X, y)

    # Save model
    joblib.dump(clf, MODEL_PATH)

    print("✅ ML model trained and saved to:", MODEL_PATH)


if __name__ == "__main__":
    train_model()
