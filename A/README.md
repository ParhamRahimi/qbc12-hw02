# HW02 — ETL Pipeline

Parham Rahimi

## Note about credentials

My name wasn't in the credentials file (qbc12_hw01_student_credentials.xlsx), so I used the first entry (Nazanin Hesari - student_nazanin_hesari) as instructed.

## Files

```
├── README.md
├── .gitignore
├── requirements.txt
├── notebooks/
│   └── 01_etl_pipeline_student.ipynb
└── data/
    └── features/
        └── .gitkeep
```

## How to run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export PGUSER=student_nazanin_hesari
export PGPASSWORD=AJsl6KVqVavYZm3bEO

jupyter nbconvert --to notebook --execute --inplace notebooks/01_etl_pipeline_student.ipynb
```

Or open the notebook in Jupyter and run cells manually.

## What the notebook does

Loads data from the QBC12 Airbnb database, builds features from listings/hosts/reviews/calendar, creates a binary target (high_demand_proxy based on future availability), validates the output, and saves versioned CSV/Parquet/JSON files to data/features/.

