from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os
import sys
sys.path.append("/opt/airflow/scripts")

from extract import extract_student_data
from transform import load_and_transform
from load import load_to_sqlite

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
    'email_on_success': False,
}

with DAG(
    dag_id="etl_pipeline",
    default_args=default_args,
    description="ETL pipeline for UCI student performance dataset",
    start_date=datetime(2025, 4, 10),
    schedule='@daily',
    catchup=False
    
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_student_data
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=load_and_transform
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_to_sqlite
    )
    extract >> transform >> load