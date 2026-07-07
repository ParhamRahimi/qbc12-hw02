# Part B — MLflow Experiment Tracking

Parham Rahimi

## What this does

Trains multiple models on the Part A dataset and tracks them in MLflow.

## Runs

- v0_leaky_logistic_regression (leaky — uses future_available_rate_30d)
- v1_dummy_baseline (DummyClassifier)
- v2_clean_logistic_regression
- v3_balanced_logistic_regression
- v4_threshold (0.30, 0.40, 0.50, 0.60)
- v5_random_forest

## Setup

```bash
cd B
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

jupyter nbconvert --to notebook --execute --inplace 02_mlflow_experiments_student.ipynb
```

## Note

MLflow credentials (nazanin_hesari@qbc12.local) are used from the same entry as Part A. When the MLflow server returns 401, tracking falls back to a local SQLite file.