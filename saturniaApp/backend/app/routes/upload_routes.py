from flask import Blueprint, request, send_file, render_template, redirect, url_for, session, make_response
from werkzeug.utils import secure_filename
from io import BytesIO
import os
import zipfile
from ..utils.process_and_send_files import process_and_send_files
from ..utils.save_data_to_db import save_data_to_db
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///databases/CFE_Recibos_DB.sqlite')

bp = Blueprint('saturnia', __name__, url_prefix='/saturnia')

@bp.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('pdfs', filename)
        file.save(file_path)

        destination_path = os.path.join('pdfs', 'extracted')
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_path)

        files = os.listdir(destination_path)
        total_files = len(files)
        processed_files = 0

        session['total_files'] = total_files
        session['processed_files'] = processed_files
        
        # Add to destination_path the current execution location before destination_path
        destination_path = os.path.join(os.getcwd(), destination_path)

        df = process_and_send_files(destination_path)

        save_data_to_db(engine, df)
        processed_files += 1
        session['processed_files'] = processed_files

        csv_data = df.to_csv(index=True, index_label='recibo').encode()

        session['csv_data'] = csv_data  # Store the CSV data in the session

        return redirect(url_for('saturnia.download'))

    return 'Upload complete', 200

@bp.route('/download', methods=['GET', 'POST'])
def download():
    # print(session)
    csv_data = session.pop('csv_data', None)  # Retrieve the CSV data from the session
    if csv_data:
        response = make_response(csv_data)
        print(response)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=recibos_data.csv'
        return response
    else:
        return redirect(url_for('saturnia.home'))

@bp.route('/refresh', methods=['GET'])
def refresh():
    return redirect(url_for('saturnia.home'))