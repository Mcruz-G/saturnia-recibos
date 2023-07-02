from flask import Blueprint, request, send_file, render_template, redirect, url_for, session, make_response
from process_and_send_files import process_and_send_files
from save_data_to_db import save_data_to_db
from sqlalchemy import create_engine
import pandas as pd
import os
import time
from werkzeug.utils import secure_filename
import shutil

# engine = create_engine('sqlite:///databases/CFE_Recibos_DB.sqlite')

bp = Blueprint('saturnia', __name__, url_prefix='/saturnia')

@bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@bp.route('/upload', methods=['POST'])
def upload():
    # Delete the contents of the 'pdfs' directory
    shutil.rmtree('pdfs')
    os.mkdir('pdfs')

    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('pdfs', filename)
        file.save(file_path)

        df = process_and_send_files([file_path])

        save_data_to_db(df)

        csv_data = df.to_csv(index=True, index_label='recibo').encode()
        
        session['csv_data'] = csv_data  # Store the CSV data in the session
        session.modified = True  # This line is added to inform Flask that the session object has been modified

        return 'Upload complete', 200

    return 'Upload failed', 400

@bp.route('/download', methods=['GET'])
def download():
    csv_data = session.get('csv_data')  # Retrieve the CSV data from the session
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