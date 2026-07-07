#!/bin/bash
# Run the FastAPI server locally
# Fill these values from the MLflow credentials sheet.
export MLFLOW_TRACKING_URI="http://185.50.38.163:33014"
export MLFLOW_TRACKING_USERNAME="nazanin_hesari@qbc12.local"
export MLFLOW_TRACKING_PASSWORD="Zdx6j6qOCsoHVk1iRD"
export STUDENT_USERNAME="nazanin_hesari"
export MLFLOW_EXPERIMENT_NAME="qbc12_hw02_student_nazanin_hesari"
export MLFLOW_RUN_ID=""
export PREDICTION_THRESHOLD="0.5"

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000