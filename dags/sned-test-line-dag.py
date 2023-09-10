from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from includes.vs_modules.check_weekday import check_weekday
from includes.vs_modules.get_stock_data import get_stock_data_31day
from includes.vs_modules.send_line_notify import lineNotifyMessage

args = {
    'owner': 'Quan-En Li',
    'start_date': days_ago(1) # make start date in the past
}

dag = DAG(
    dag_id='send-test-line-dag',
    default_args=args,
    schedule_interval='@daily' # make this workflow happen every day
)

with dag:
    tw_stock_start = DummyOperator(
        task_id='tw_stock_start'
    )

    check_weekday = BranchPythonOperator(
        task_id='check_weekday',
        python_callable=check_weekday,
        op_args=['{{ ds_nodash }}']
    )

    is_holiday = DummyOperator(
        task_id='is_holiday'
    )

    is_workday = DummyOperator(
        task_id='is_workday'
    )

    get_stock_info = PythonOperator(
        task_id='get-stock-info',
        python_callable=get_stock_data_31day,
        op_args=['2330.TW'],
        provide_context=True,
    )

    send_mesg = PythonOperator(
        task_id='line-notify',
        python_callable=lineNotifyMessage,
        op_args=["test123", None],
        trigger_rule="one_success"
    )

    tw_stock_end = DummyOperator(
        task_id='tw_stock_end',
        trigger_rule='one_success'
    )

    tw_stock_start >> check_weekday >> [is_workday, is_holiday]
    is_workday >> send_mesg >> tw_stock_end
    is_holiday >> get_stock_info >> send_mesg >> tw_stock_end