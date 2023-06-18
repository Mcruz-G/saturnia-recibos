import streamlit as st
from docaiprocess import process_document  # Import the function you've developed
from sqlalchemy import create_engine, inspect, text
import pandas as pd
import os

def front_page():

    st.markdown("# Saturnia Receipts App", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        h1{
        font-size:60px !important;
        color:#DFFF00;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("""

    Put here your client's recipts and summarize them into an excel! 

    To introduce a .zip file:

    1. Click on the 'Browse files' button below.
    2. Navigate to the location of your .zip file in the file dialog.
    3. Select the .zip file and click 'Open'.
    """)



def process_and_send_files():
    fields = {}
    files = os.listdir('recibos')
    with st.spinner('Processing...'):
        for i, filename in enumerate(files):
            if filename.endswith('.pdf'):
                name = filename.split(".")[0]
                file_path = os.path.join('recibos', filename)
                result = process_document(file_path)
                fields[name] = result

    df = pd.DataFrame.from_dict(fields, orient='index')
    csv = df.to_csv(index=True, index_label="recibo").encode()

    st.success('Done!')
    st.download_button(label="Download Results as CSV", data=csv, file_name='recibos_data.csv', mime='text/csv')
    return df


def save_data_to_db(engine, df):
    inspector = inspect(engine)
    with engine.connect() as connection:
        df.to_sql('recibos', connection, index=True, index_label='recibo', if_exists='append')
        result = connection.execute(text("SELECT DISTINCT * FROM recibos LIMIT 10"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        # Query the database to get the first 10 rows from 'recibos' table
        st.markdown('Collect your clients data into your database. Until now, these are the first 10 rows that you have collected so far:')
        st.dataframe(df)