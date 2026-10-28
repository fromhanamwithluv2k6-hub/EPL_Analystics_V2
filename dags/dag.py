from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.python import PythonOperator
from etl_scripts.crawler import PLdataUpdate
from etl_scripts.import_to_db import update_data
from etl_scripts.main_poisson import run_predict_model

def crawl_schedule_task():
    extract = PLdataUpdate()
    extract.update_schedule()

def crawl_standings_task():
    extract = PLdataUpdate()
    extract.update_standings()

def crawl_match_stat_task():
    extract = PLdataUpdate()
    extract.update_schedule() 

def crawl_teams_task():
    extract = PLdataUpdate()
    extract.update_teams()

def crawl_players_profile_task():
    extract = PLdataUpdate()
    extract.update_players_profile()

def update_players_stat_task():
    extract = PLdataUpdate()
    extract.update_players_stat()

def load_to_database_task():
    load = update_data()
    load.upsert_all()

def run_predict_task():
    run_predict_model()

def load_predict_to_database_task():
    load = update_data()
    load.upsert_predictions_table()

def close_database_task():
    load = update_data()
    load.close_connection()

default_args = {
    'owner': 'SDY',
    'retries': 5,
    'retry_delay': timedelta(minutes=2) 
}

with DAG(
    dag_id='dag_for_EPL_analystics_project',
    default_args=default_args,
    start_date=datetime(2026, 10, 10, 2),
    schedule='0 0 * * 4',
    catchup=True
) as dag:
    task1 = PythonOperator(
        task_id='crawl_schedule',
        python_callable=crawl_schedule_task
    )
    
    task2 = PythonOperator(
        task_id='crawl_standings',
        python_callable=crawl_standings_task
    )
    
    task3 = PythonOperator(
        task_id='crawl_match_stat',
        python_callable=crawl_match_stat_task   
    )
    
    task4 = PythonOperator(
        task_id='crawl_teams',
        python_callable=crawl_teams_task
    )
    
    task5 = PythonOperator(
        task_id='crawl_players_profile',
        python_callable=crawl_players_profile_task
    )
    
    task6 = PythonOperator(
        task_id='update_players_stat',
        python_callable=update_players_stat_task
    )
    
    task7 = PythonOperator(
        task_id='load_to_database',
        python_callable=load_to_database_task
    )
    
    task8 = PythonOperator(
        task_id='run_the_predict',
        python_callable=run_predict_task
    )
    
    task9 = PythonOperator(
        task_id='load_predict_to_database',
        python_callable=load_predict_to_database_task
    )
    
    task10 = PythonOperator(
        task_id='close_database',
        python_callable=close_database_task
    )
    [task1, task2, task3, task4, task5, task6] >> task7
    task7 >> task8
    task8 >> task9
    task9 >> task10