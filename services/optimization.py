import numpy as np
from ml.model_store import load_model


# Combine ML score with business rules (lead time, tech capacity, center day cap)


def rank_slots(available_slots, service_minutes=60):
model = load_model()
scored = []
for s in available_slots:
feats = np.array([[s["remaining"], service_minutes]])
ml_score = float(model.predict_proba(feats)[0,1]) if model else 0.5
# Business rule bonus: prefer slots with some headroom but not empty
headroom = 1.0 if 1 <= s["remaining"] <= 2 else 0.6 if s["remaining"]>2 else 0.0
score = 0.7*ml_score + 0.3*headroom
scored.append({**s, "score": round(score,3)})
return sorted(scored, key=lambda x: x["score"], reverse=True)
