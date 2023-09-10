from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from includes.vs_modules.send_line_notify import lineNotifyMessage
from includes.vs_modules.check_weekday import check_weekday
from includes.vs_modules.get_stock_data import get_stock_data_31day
from includes.vs_modules.plot_kd_index import plot_kd_index_2_file


def send_mesg(**context):
    img_path = context['task_instance'].xcom_pull(task_ids='plot-KD-index')
    lineNotifyMessage(msg="2330", img_path=img_path)

def plot_kd(**context):
    df = context['task_instance'].xcom_pull(task_ids='get-stock-info')
    img_path = plot_kd_index_2_file(df, title="KD - 2330")
    return img_path

args = {
    'owner': 'Quan-En Li',
    'start_date': days_ago(1) # make start date in the past
}

dag = DAG(
    dag_id='send-mesg-dag',
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
        op_args=['2330'],
        provide_context=True,
    )

    plot_kd = PythonOperator(
        task_id='plot-KD-index',
        python_callable=plot_kd,
        provide_context=True,
    )

    send_mesg = PythonOperator(
        task_id='line-notify',
        python_callable=send_mesg,
    )

    tw_stock_end = DummyOperator(
        task_id='tw_stock_end',
        trigger_rule='one_success'
    )

    tw_stock_start >> check_weekday >> [is_workday, is_holiday]
    is_holiday >> get_stock_info >> plot_kd >> send_mesg >> tw_stock_end
    is_workday >> tw_stock_end