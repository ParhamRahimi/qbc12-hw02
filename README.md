# QBC12 MLOps — Homework 02

Parham Rahimi

## Note

My name wasn't in the credentials file (qbc12_hw01_student_credentials.xlsx), so I used the first entry (Nazanin Hesari) for all parts.

## Parts

- **Part A** — ETL pipeline: extracts data from PostgreSQL, builds features, saves clean dataset to `data/features/`
- **Part B** — MLflow experiments: trains 8 model variants (leaky, dummy, LR, balanced LR, tuned thresholds, Random Forest), tracks them, selects best clean run
- **Part C** — FastAPI serving: serves the selected model via REST API with Swagger docs, validates inputs, rejects leakage fields

Each part has its own README with setup and usage instructions.