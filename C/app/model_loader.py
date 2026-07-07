import os
import json
from pathlib import Path
import mlflow
import mlflow.sklearn

# Columns the model expects (from Part A ETL - clean features only)
EXPECTED_FEATURES = [
    "property_type", "room_type", "accommodates", "bathrooms",
    "bedrooms", "beds", "listing_price", "minimum_nights",
    "maximum_nights", "instant_bookable", "is_superhost",
    "host_listing_count", "neighbourhood_name",
    "total_reviews_before_cutoff", "unique_reviewers_before_cutoff",
    "avg_comment_len_before_cutoff", "max_comment_len_before_cutoff",
    "days_since_last_review",
    "calendar_days_observed_last_90d", "available_days_last_90d",
    "available_rate_last_90d", "avg_minimum_nights_calendar_last_90d",
    "avg_maximum_nights_calendar_last_90d",
    "calendar_days_observed_last_30d", "available_days_last_30d",
    "available_rate_last_30d", "avg_minimum_nights_calendar_last_30d",
    "avg_maximum_nights_calendar_last_30d",
]

_model = None
_model_info = {
    "model_type": "RandomForestClassifier",
    "feature_count": len(EXPECTED_FEATURES),
    "features": EXPECTED_FEATURES,
    "threshold": 0.5,
    "mlflow_run_id": None,
}


def load_model():
    """Try loading from MLflow, fall back to local artifact."""
    global _model, _model_info

    # Try remote MLflow
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://185.50.38.163:33014")
    username = os.getenv("MLFLOW_TRACKING_USERNAME", "nazanin_hesari@qbc12.local")
    password = os.getenv("MLFLOW_TRACKING_PASSWORD", "Zdx6j6qOCsoHVk1iRD")
    run_id = os.getenv("MLFLOW_RUN_ID", "")

    if run_id:
        os.environ["MLFLOW_TRACKING_USERNAME"] = username
        os.environ["MLFLOW_TRACKING_PASSWORD"] = password
        mlflow.set_tracking_uri(tracking_uri)
        try:
            _model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
            _model_info["mlflow_run_id"] = run_id
            print(f"Loaded model from MLflow run {run_id}")
            return _model
        except Exception as e:
            print(f"MLflow load failed: {e}, trying local fallback...")

    # Fall back to local SQLite
    local_db = Path("artifacts/mlflow.db")
    if local_db.exists():
        mlflow.set_tracking_uri(f"sqlite:///{local_db.absolute()}")
        try:
            # Find best v5 run
            client = mlflow.tracking.MlflowClient()
            exp = client.get_experiment_by_name(
                "qbc12_hw02_student_nazanin_hesari"
            )
            if exp:
                runs = mlflow.search_runs(
                    [exp.experiment_id],
                    filter_string="tags.leakage_status = 'clean'",
                    order_by=["metrics.f1 DESC"],
                )
                if len(runs) > 0:
                    best_run_id = runs.iloc[0]["run_id"]
                    _model = mlflow.sklearn.load_model(
                        f"runs:/{best_run_id}/model"
                    )
                    _model_info["mlflow_run_id"] = best_run_id
                    print(f"Loaded from local DB, run {best_run_id}")
                    return _model
        except Exception as e:
            print(f"Local MLflow fallback failed: {e}")

    print("WARNING: Model not loaded. Endpoints will return errors.")
    return None


def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model


def get_model_info():
    return _model_info