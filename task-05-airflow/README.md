# Task 05 - Airflow

## Task description

Two Airflow DAGs that process a CSV file and load it into MongoDB:

1. **Processing DAG** - a sensor waits for the data file, a branch checks whether
   the file is empty, and a TaskGroup cleans the data (replaces nulls, sorts by
   `created_date`, removes unwanted characters from `content`).
2. **Loading DAG** - triggered by the processed dataset (data-aware scheduling),
   loads the result into MongoDB.

Airflow and MongoDB run locally in Docker.
