# coding: utf-8
"""A DAG to test cdo select operator.

Example
-------
Run the following command to test:
   $ airflow trigger_dag \
     --conf "$(jq '.' ./common_example.json)" \
     ploto_processor_cdo_select
"""
import airflow.utils.dates
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

from ploto_airflow.operators.processor.cdo_processor.select import (
    generate_operator as generate_cdo_select_operator
)
from ploto_airflow.esmdiag.climo.util import generate_cdo_select_params


args = {
    "owner": "ploto",
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
}


dag_id = "ploto_processor_cdo_select"


with DAG(
    dag_id=dag_id,
    default_args=args,
    schedule_interval=None,
) as dag:
    show_task = BashOperator(
        task_id="show_date",
        bash_command='date',
        dag=dag,
    )

    run_task_id = "run_cdo_select"
    run_task = generate_cdo_select_operator(run_task_id, generate_cdo_select_params, "PS")
    run_task.dag = dag

    run_task.set_upstream(show_task)
