import pandas as pd
from app.model_loader import get_model, get_model_info


def predict(features: dict):
    """Predict for a single instance."""
    model = get_model()
    if model is None:
        raise RuntimeError("Model not loaded. Please check MLflow configuration.")

    # Convert features dict to DataFrame with correct column order
    info = get_model_info()
    expected = info["features"]
    threshold = float(info.get("threshold", 0.5))

    # Ensure all expected features are present
    missing = [f for f in expected if f not in features]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    # Build DataFrame
    df = pd.DataFrame([features])[expected]

    # Get probability
    proba = model.predict_proba(df)[:, 1][0]
    pred = int(proba >= threshold)

    return {
        "prediction": pred,
        "probability": round(float(proba), 6),
        "high_demand_proxy": bool(pred),
    }


def predict_batch(instances: list[dict]):
    """Predict for multiple instances."""
    model = get_model()
    if model is None:
        raise RuntimeError("Model not loaded. Please check MLflow configuration.")

    info = get_model_info()
    expected = info["features"]
    threshold = float(info.get("threshold", 0.5))

    results = []
    for i, instance in enumerate(instances):
        missing = [f for f in expected if f not in instance]
        if missing:
            raise ValueError(
                f"Instance {i} is missing required features: {missing}"
            )
        results.append(instance)

    df = pd.DataFrame(results)[expected]
    probas = model.predict_proba(df)[:, 1]

    predictions = []
    for proba in probas:
        pred = int(proba >= threshold)
        predictions.append({
            "prediction": pred,
            "probability": round(float(proba), 6),
            "high_demand_proxy": bool(pred),
        })

    return predictions