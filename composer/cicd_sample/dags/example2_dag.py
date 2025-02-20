# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

from airflow import models
from airflow.operators import bash
from airflow.operators.python_operator import PythonOperator

# If you are running Airflow in more than one time zone
# see https://airflow.apache.org/docs/apache-airflow/stable/timezone.html
# for best practices
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    "owner": "Composer Example 2",
    "depends_on_past": False,
    "email": [""],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "start_date": YESTERDAY,
}


def get_secret_data():

    project_id = "tn-data-dept2-test-proj"
    secret_id = "spoke_1_airflow_variables"
    version_id = 'latest'
    
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    secret_detail = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(secret_detail)
    data = response.payload.data.decode("UTF-8")
    # print("Data: {}".format(data))
    return data

'''
with models.DAG(
    "composer_sample_dag_2",
    "catchup=False",
    default_args=default_args,
    schedule_interval=datetime.timedelta(days=1),
) as dag:

    # Print the dag_run id from the Airflow logs
    print_dag_run_conf = bash.BashOperator(
        task_id="print_dag_run_conf", bash_command="pip freeze"
        # echo spoke_1_airflow_variables: {temp}"
    )

def my_function():
    print("hello world")
    print(foo)
    return 0
'''

with models.DAG(
    'example_2_dag_spoke_1',
    catchup=False,
    default_args=default_args,
    schedule_interval=datetime.timedelta(days=1)) as dag:

    # Print the dag_run id from the Airflow logs
    t1 = PythonOperator(
        task_id='print',
        python_callable= get_secret_data,
        dag=dag,
        )
