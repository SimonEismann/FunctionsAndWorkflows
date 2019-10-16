from datetime import datetime
import requests 
import base64
import uuid
import os
import json
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook


def input_arg(**kwargs):
    try:
        mess = kwargs['dag_run'].conf["message"]
        print("Retrieved: "+str(mess))
        return mess
    except:
        print("Could not read input value. Defaulting to 'Hello World!'")
        return "Hello World!"


def text2speech(**kwargs):
    ti = kwargs['ti']
    data = {"message": ti.xcom_pull(task_ids="input")}
    response = requests.post("https://us-central1-devops-218113.cloudfunctions.net/Text2Speech", json=data)
    fileName = str(uuid.uuid4())
    with open(fileName, "wb") as outfile:
        outfile.write(response.content)

    gcs = GoogleCloudStorageHook()
    gcs.upload("workflowstorage", fileName, fileName, mime_type='application/octet-stream')

    os.remove(fileName)
    return fileName


def conversion(**kwargs):
    ti = kwargs['ti']
    fileName = ti.xcom_pull(task_ids="text2speech")
    gcs = GoogleCloudStorageHook()
    gcs.download("workflowstorage", fileName, fileName)
    file = open(fileName, 'rb').read()
    response = requests.post("https://us-central1-devops-218113.cloudfunctions.net/Conversion", data=file)
    newFileName = str(uuid.uuid4())
    with open(newFileName, "wb") as outfile:
        outfile.write(response.content)
    gcs.upload("workflowstorage", newFileName, newFileName, mime_type='application/octet-stream')
    os.remove(newFileName)
    return newFileName


def profanity(**kwargs):
    ti = kwargs['ti']
    data = {"message": ti.xcom_pull(task_ids="input")}
    response = requests.post("https://us-central1-devops-218113.cloudfunctions.net/Profanity-Detection", json=data)
    return json.loads(response.content)["indexes"]


def censor(**kwargs):
    ti = kwargs['ti']
    indexes = ti.xcom_pull(task_ids="profanity")
    fileName = ti.xcom_pull(task_ids="compression")
    gcs = GoogleCloudStorageHook()
    gcs.download("workflowstorage", fileName, fileName)
    message = {"to_censor" : open(fileName, 'rb'), "indexes" : json.dumps(indexes)}
    response = requests.post("https://us-central1-devops-218113.cloudfunctions.net/Censor", files=message)
    newFileName = str(uuid.uuid4())
    with open(newFileName, "wb") as outfile:
        outfile.write(response.content)
    gcs.upload("workflowstorage", newFileName, newFileName, mime_type='application/octet-stream')
    os.remove(newFileName)
    return newFileName


def compression(**kwargs):
    ti = kwargs['ti']
    fileName = ti.xcom_pull(task_ids="conversion")
    gcs = GoogleCloudStorageHook()
    gcs.download("workflowstorage", fileName, fileName)
    file = {"to_compress" : open(fileName, 'rb')}
    response = requests.post("https://us-central1-devops-218113.cloudfunctions.net/Compression", files=file)
    newFileName = str(uuid.uuid4())
    with open(newFileName, "wb") as outfile:
        outfile.write(response.content)
    gcs.upload("workflowstorage", newFileName, newFileName, mime_type='application/octet-stream')
    os.remove(newFileName)
    return newFileName


def cleanup(**kwargs):
    ti = kwargs['ti']
    gcs = GoogleCloudStorageHook()
    fileName = ti.xcom_pull(task_ids="censor")
    gcs.delete("workflowstorage", fileName)
    fileName = ti.xcom_pull(task_ids="compression")
    gcs.delete("workflowstorage", fileName)
    fileName = ti.xcom_pull(task_ids="conversion")
    gcs.delete("workflowstorage", fileName)
    fileName = ti.xcom_pull(task_ids="text2speech")
    gcs.delete("workflowstorage", fileName)


dag = DAG('CompressFirst', description='Audio workflow',
          schedule_interval=None,
          start_date=datetime(2017, 2, 1),
          catchup=False)

censor = PythonOperator(task_id='censor', python_callable=censor, dag=dag, provide_context=True)
input_arg = PythonOperator(task_id='input', python_callable=input_arg, dag=dag, provide_context=True)
text2speech = PythonOperator(task_id='text2speech', python_callable=text2speech, dag=dag, provide_context=True)
conversion = PythonOperator(task_id='conversion', python_callable=conversion, dag=dag, provide_context=True)
profanity = PythonOperator(task_id='profanity', python_callable=profanity, dag=dag, provide_context=True)
compression = PythonOperator(task_id='compression', python_callable=compression, dag=dag, provide_context=True)
cleanup = PythonOperator(task_id='cleanup', python_callable=cleanup, dag=dag, provide_context=True)

input_arg >> [profanity, text2speech] >> conversion >> compression >> censor >> cleanup