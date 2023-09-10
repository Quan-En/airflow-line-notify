FROM apache/airflow:2.7.1-python3.11
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt
COPY best_four_point.py /home/airflow/.local/lib/python3.11/site-packages/twstock/cli/best_four_point.py