import os
from process_document import process_document
import pandas as pd

from google.cloud import bigquery
import google 



def save_data_to_bigquery(df):
    project_id = "saturnia-recibos"
    dataset_name = "saturnia_app"
    table_name = "recibos"
    credentials = google.oauth2.service_account.Credentials.from_service_account_file(
        'keys/key_docai.json')
    client = bigquery.Client(credentials=credentials)
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)

    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
    job_config.autodetect = True

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"Data saved to BigQuery table: {project_id}.{dataset_name}.{table_name}")


def process_and_send_files(dir):
    fields = {}
    # if isinstance(file_paths, str):
    #     file_paths = [file_paths]
        
    # for file_paths in dir
    for file_path in os.listdir(dir):
        if file_path.endswith('.pdf'):
            name = os.path.basename(file_path).split(".")[0]
            result = process_document(file_path)
            fields[name] = result

    df = pd.DataFrame.from_dict(fields, orient='index')
    return df