# Part C — FastAPI Model Serving

Parham Rahimi

Serves the Random Forest model from Part B via FastAPI.

## Endpoints

- `GET /` — root message
- `GET /health` — model loaded status
- `GET /model-info` — model type, features, threshold
- `POST /predict` — single prediction
- `POST /predict-batch` — batch prediction

Swagger: http://127.0.0.1:8000/docs

## Setup

```bash
cd C
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the server
source run_local.sh
```

## Notes

Uses Nazanin Hesari's credentials (same as Parts A/B). Falls back to local SQLite MLflow DB in `artifacts/` when the remote server is unreachable. The best run from Part B (v5_random_forest) is auto-selected.