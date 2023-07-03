from flask import Blueprint, request, send_file, render_template, redirect, url_for, session, make_response
from process_and_send_files import process_and_send_files
from save_data_to_db import save_data_to_db
from sqlalchemy import create_engine
import pandas as pd
import os
import time
from werkzeug.utils import secure_filename
import shutil
import google 
from google.cloud import bigquery



def save_identifier(identifier):
    with open('processed_files_identifiers.txt', 'a') as f:
        f.write(identifier + '\n')

def get_processed_identifiers():
    with open('processed_files_identifiers.txt', 'r') as f:
        identifiers = f.read().splitlines()
    return identifiers

# engine = create_engine('sqlite:///databases/CFE_Recibos_DB.sqlite')
bp = Blueprint('saturnia', __name__, url_prefix='/saturnia')

@bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@bp.route('/upload', methods=['POST'])
def upload():
    user_id = request.remote_addr + request.user_agent.string
    
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('pdfs', filename)
        # Add current path to file_path
        file_path = os.path.join(os.getcwd(), file_path)
        # print(file_path)
        file.save(file_path)



        df = process_and_send_files(file_path)

        save_data_to_db(df, user_id)

        # Delete .pdf part of the filename
        filename = filename[:-4]
        save_identifier(filename)
        return 'Upload complete', 200

    return 'Upload failed', 400

@bp.route('/download', methods=['GET'])
def download():
    # Get IP and User Agent
    user_id = request.remote_addr + request.user_agent.string

    project_id = 'saturnia-recibos'
    dataset_id = 'saturnia_app'
    table = 'recibos'


    query = f"""
            SELECT * FROM {project_id}.{dataset_id}.{table}
            WHERE user_id = {user_id}
            """

    print(query)
    credentials = google.oauth2.service_account.Credentials.from_service_account_file(
        os.path.join(os.getcwd(), 'keys/key_docai.json'))
    
    client = bigquery.Client(credentials=credentials)
    df = client.query(query).to_dataframe()

    csv_data = df.to_csv(index=True).encode()
    if csv_data:
        response = make_response(csv_data)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=recibos_data.csv'
        return response
    else:
        return 'No CSV data found', 400


@bp.route('/refresh', methods=['GET'])
def refresh():
    return redirect(url_for('saturnia.home'))