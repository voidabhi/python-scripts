from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 1, 1),
    'email': ['mymail@mail.net'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    }

python = "/usr/bin/python"
env = { "CLOUDSDK_PYTHON": python, "BEAM_PYTHON": python }

dag = DAG('dataflow_bigquery', schedule_interval='*/10 * * * *', default_args=default_args)

dataflow_batch = BashOperator(
    task_id='dataflow_batch',
    bash_command='python /usr/bin/dataflow',
    xcom_push='true',
    dag=dag,
    env=env)

batch_processor = BashOperator(
    task_id='batch_processor',
    bash_command="python /usr/bin/bigquery {{ ti.xcom_pull(task_ids='dataflow_batch') }}",
    retries=3,
    dag=dag,
    env=env)

batch_processor.set_upstream(dataflow_batch)
