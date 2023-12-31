import os
from process_document import process_document
import pandas as pd

from google.cloud import bigquery
import google 



def save_data_to_bigquery(df):
    project_id = "saturnia-recibos"
    dataset_name = "saturnia_app"
    table_name = "recibos"

    keys_path = os.path.join(os.getcwd(), 'keys/key_docai.json')
    credentials = google.oauth2.service_account.Credentials.from_service_account_file(keys_path)
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


def process_and_send_files(file_path):
    fields = {}
    if file_path.endswith('.pdf'):
        #build absolute file_path 
        name = os.path.basename(file_path).split(".")[0]
        result = process_document(file_path)
        fields[name] = result

    df = pd.DataFrame.from_dict(fields, orient='index',)
    df.index.name = 'recibo'
    return df