from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any


# Columns that must NOT be accepted in prediction requests (leakage/audit/target)
FORBIDDEN_PREDICTION_FIELDS = {
    "listing_id",
    "cutoff_date",
    "dataset_version",
    "future_calendar_days_observed_30d",
    "future_available_days_30d",
    "future_available_rate_30d",
    "high_demand_proxy",
}


class PredictionRequest(BaseModel):
    features: Dict[str, Any]

    @field_validator("features")
    @classmethod
    def check_forbidden_fields(cls, v):
        found = [f for f in FORBIDDEN_PREDICTION_FIELDS if f in v]
        if found:
            raise ValueError(
                f"Forbidden fields detected: {found}. "
                f"These are audit, future-window, or target columns."
            )
        return v


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    high_demand_proxy: bool


class BatchPredictionRequest(BaseModel):
    instances: List[Dict[str, Any]]

    @field_validator("instances")
    @classmethod
    def check_forbidden_fields(cls, v):
        for i, instance in enumerate(v):
            found = [f for f in FORBIDDEN_PREDICTION_FIELDS if f in instance]
            if found:
                raise ValueError(
                    f"Instance {i} has forbidden fields: {found}. "
                    f"These are audit, future-window, or target columns."
                )
        return v


class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


class ModelInfoResponse(BaseModel):
    model_type: str
    feature_count: int
    features: List[str]
    mlflow_run_id: Optional[str] = None
    threshold: float