import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.schemas import (
    PredictionRequest, PredictionResponse,
    BatchPredictionRequest, BatchPredictionResponse,
    HealthResponse, ModelInfoResponse,
)
from app.predictor import predict, predict_batch
from app.model_loader import get_model_info

app = FastAPI(
    title="Airbnb Availability Predictor",
    description="Serves the HW02 Random Forest model for predicting high-demand listings.",
    version="1.0.0",
)

PREDICTION_THRESHOLD = float(os.getenv("PREDICTION_THRESHOLD", "0.5"))


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )


@app.get("/")
def root():
    return {"message": "Airbnb Availability Predictor API", "docs": "/docs"}


@app.get("/health", response_model=HealthResponse)
def health():
    from app.model_loader import get_model
    model = get_model()
    return HealthResponse(
        status="ok" if model else "model_not_loaded",
        model_loaded=model is not None,
    )


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    info = get_model_info()
    return ModelInfoResponse(**info)


@app.post("/predict", response_model=PredictionResponse)
def single_predict(request: PredictionRequest):
    try:
        result = predict(request.features)
        return PredictionResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/predict-batch", response_model=BatchPredictionResponse)
def batch_predict(request: BatchPredictionRequest):
    try:
        predictions = predict_batch(request.instances)
        return BatchPredictionResponse(predictions=predictions)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))