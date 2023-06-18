import streamlit as st
import zipfile
import os
import pandas as pd
import shutil
import base64
from docaiprocess import process_document  # Import the function you've developed
from sqlalchemy import create_engine, inspect, text
from utils import front_page, process_and_send_files, save_data_to_db


# Create a SQLAlchemy engine connected to a SQLite database
engine = create_engine('sqlite:///databases/CFE_Recibos_DB.sqlite')

# Create the front page UI
front_page()

uploaded_file = st.file_uploader("Upload file", type=['zip'])

if uploaded_file is not None:
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # This will exclude any directories
                if not member.endswith('/'):
                    zip_ref.extract(member, 'recibos')

    output_data = process_and_send_files()

    save_data_to_db(engine, output_data)
