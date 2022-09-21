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

def get_secret(project_id, secret_id):
    """
    Get information about the given secret. This only returns metadata about
    the secret container, not any secret material.
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = client.secret_path(project_id, secret_id)

    # Get the secret.
    response = client.get_secret(request={"name": name})

    # Get the replication policy.
    if "automatic" in response.replication:
        replication = "AUTOMATIC"
    elif "user_managed" in response.replication:
        replication = "MANAGED"
    else:
        raise "Unknown replication {}".format(response.replication)

    # Print data about the secret.
    print("Got secret {} with replication policy {}".format(response.name, replication))
    return response.name

temp = get_secret("tn-data-dept2-test-proj", "spoke_1_airflow_variables")
    
with models.DAG(
    "composer_sample_dag_2",
    "catchup=False",
    default_args=default_args,
    schedule_interval=datetime.timedelta(days=1),
) as dag:

    # Print the dag_run id from the Airflow logs
    print_dag_run_conf = bash.BashOperator(
        task_id="print_dag_run_conf", bash_command=f"echo spoke_1_airflow_variables: {temp}"
    )
