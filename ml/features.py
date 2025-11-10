import pandas as pd


def make_features(df: pd.DataFrame):
# df columns: remaining, service_minutes, label (1=good slot, 0=bad)
X = df[["remaining", "service_minutes"]]
y = df["label"]
return X, y

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from .features import make_features
from .model_store import MODEL_PATH


# synthetic training set for demo


df = pd.DataFrame({
"remaining": [0,1,2,3,4,1,2,3,0,4,2,1,3,4,2,1],
"service_minutes": [60,60,60,60,60,90,90,30,30,45,120,45,60,30,60,90],
"label": [0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1]
})


X, y = make_features(df)
clf = RandomForestClassifier(n_estimators=60, random_state=42)
clf.fit(X, y)
joblib.dump(clf, MODEL_PATH)
print("Model trained ->", MODEL_PATH)

import os, joblib
MODEL_PATH = os.path.join("ml", "slot_rf.pkl")


def load_model():
if os.path.exists(MODEL_PATH):
return joblib.load(MODEL_PATH)
return None
