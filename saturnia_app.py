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
        counter = 0
        for member in zip_ref.namelist():
            
            file_basename = os.path.basename(member)
            destination_path = 'recibos'
            # Check if the directory exists
            if os.path.exists(destination_path) and counter == 0:
                # If it does exist, delete it
                shutil.rmtree(destination_path)
                counter += 1

                # In either case, create the destination_path
                os.makedirs(destination_path)
            else:
                if counter == 0:
                    os.makedirs(destination_path)


            source = zip_ref.open(member)
            target = open(os.path.join(destination_path, file_basename), "wb")
            # zip_ref.extract(member, destination_path)
            with source, target:
                shutil.copyfileobj(source, target)

            
    output_data = process_and_send_files()

    save_data_to_db(engine, output_data)
