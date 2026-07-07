# QBC12 MLOps — Homework 02 — ETL Pipeline

**Student:** Parham Rahimi

## Overview

This project implements an ETL (Extract, Transform, Load) pipeline that builds a privacy-aware ML feature dataset from the QBC12 Airbnb PostgreSQL database. The pipeline extracts raw data, engineers features from historical calendar availability and reviews, builds a binary target label, validates the output, and saves versioned artifacts.

## Credentials Note

My name (Parham Rahimi) was not listed in `qbc12_hw01_student_credentials.xlsx`. Per instructor guidance, I am using the credentials of the first entry in the file, Nazanin Hesari (`student_nazanin_hesari`), for this assignment.

## Database Status

The database server at `185.50.38.163:32112` is frequently at connection capacity during peak hours, returning:

```
FATAL: remaining connection slots are reserved for roles with the SUPERUSER attribute
```

If you encounter this error, wait a few minutes and try again, or run during off-peak hours (late night / early morning).

## Project Structure

```
A/
├── README.md
├── .gitignore
├── requirements.txt
├── notebooks/
│   └── 01_etl_pipeline_student.ipynb   # Main ETL notebook
└── data/
    └── features/                        # Output directory (populated after execution)
        ├── listing_availability_features_v1_student.csv
        ├── listing_availability_features_v1_student.parquet
        ├── listing_availability_features_v1_student_metadata.json
        ├── listing_availability_features_v1_student_validation_report.json
        └── pii_audit_v1_student.csv
```

## Setup

```bash
cd A
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Notebook

Set your database credentials as environment variables, then execute:

```bash
export PGUSER=student_nazanin_hesari
export PGPASSWORD=AJsl6KVqVavYZm3bEO
cd A
source venv/bin/activate
jupyter nbconvert --to notebook --execute --inplace notebooks/01_etl_pipeline_student.ipynb
```

Or open interactively:

```bash
cd A && source venv/bin/activate
jupyter notebook notebooks/
```

## Pipeline Steps

| Section | Description |
|---|---|
| 0. Imports | Required Python libraries |
| 1. Configuration | Dataset version, time windows, thresholds |
| 2. Database connection | Connects to QBC12 Airbnb PostgreSQL |
| 3. Data inspection | Lists tables, columns, row counts |
| 4. Quality audit | Checks date ranges, null rates, price usability |
| 5. Cutoff date | Computes valid cutoff from calendar date range |
| 6. PII audit | Identifies and documents all sensitive columns |
| 7. Extract static tables | Loads listing, host, neighbourhood tables |
| 8. Clean static fields | Boolean/numeric conversions, bathroom text parser |
| 9. Static features | Joins listing→host→neighbourhood, host_listing_count |
| 10. Review features | SQL aggregation: review counts, comment stats |
| 11. Calendar features | 90-day and 30-day availability history features |
| 12. Target label | `high_demand_proxy` binary target from future availability |
| 13. Join & assemble | Merges all feature groups, fills missing values |
| 14. Drop unusable columns | Removes >95% missing and constant columns |
| 15. Validation | Asserts: no duplicates, binary target, no PII leakage |
| 16. Save outputs | CSV, Parquet, metadata JSON, validation report, PII audit |
| 17. Final preview | Shape, head, info summary |

## Output Files

After successful execution, `data/features/` will contain:

- `listing_availability_features_v1_student.csv` — Feature dataset (CSV)
- `listing_availability_features_v1_student.parquet` — Feature dataset (Parquet)
- `listing_availability_features_v1_student_metadata.json` — ETL metadata
- `listing_availability_features_v1_student_validation_report.json` — Validation results
- `pii_audit_v1_student.csv` — PII audit table

## Dependencies

- Python 3.12+
- pandas, numpy
- SQLAlchemy + psycopg2-binary
- pyarrow (for Parquet output)
- jupyter, nbformat, nbconvert