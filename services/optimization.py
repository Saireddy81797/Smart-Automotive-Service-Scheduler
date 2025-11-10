import numpy as np
from ml.model_store import load_model


def rank_slots(available_slots, service_minutes=60):
    """
    Rank slots using ML probability + business rules.
    available_slots → list of dicts from scheduler.list_available()
    """

    model = load_model()
    ranked = []

    for slot in available_slots:
        remaining = slot.get("remaining", 0)

        # ML Features → shape (1, 2)
        features = np.array([[remaining, service_minutes]])

        if model:
            ml_score = float(model.predict_proba(features)[0][1])
        else:
            ml_score = 0.5  # fallback if model missing

        # Business rule boost
        if remaining == 0:
            business_score = 0.0
        elif remaining == 1:
            business_score = 1.0
        elif remaining == 2:
            business_score = 0.8
        else:
            business_score = 0.6

        final_score = round((ml_score * 0.7) + (business_score * 0.3), 3)

        ranked.append({
            **slot,
            "score": final_score
        })

    # highest score first
    return sorted(ranked, key=lambda x: x["score"], reverse=True)
