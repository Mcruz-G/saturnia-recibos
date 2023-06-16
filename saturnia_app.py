import streamlit as st
import zipfile
import os
import pandas as pd
import shutil
import base64
from docaiprocess import process_document  # Import the function you've developed
from sqlalchemy import create_engine, inspect, text

# Create a SQLAlchemy engine connected to a SQLite database
engine = create_engine('sqlite:///databases/CFE_Recibos_DB.sqlite')

st.markdown("# Saturnia", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    h1{
    font-size:60px !important;
    color:#6c757d;
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

uploaded_file = st.file_uploader("Upload file", type=['zip'])

# if os.path.exists('recibos') and os.path.isdir('recibos'):
#     shutil.rmtree('recibos')  # Deletes the directory

if uploaded_file is not None:
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # This will exclude any directories
                if not member.endswith('/'):
                    zip_ref.extract(member, 'recibos')

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

    inspector = inspect(engine)
    with engine.connect() as connection:
        if 'recibos' not in inspector.get_table_names():
            df.to_sql('recibos', connection, index=True, index_label="recibo")
        else:
                existing_ids = pd.read_sql('SELECT recibo FROM recibos', connection)
                df_new = df[~df.index.isin(existing_ids.index)]
                if not df_new.empty:
                    df_new.to_sql('recibos', engine, index=True, index_label='recibo', if_exists='append')

    
        result = connection.execute(text("SELECT DISTINCT * FROM recibos LIMIT 10"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

        # Query the database to get the first 10 rows from 'recibos' table
        
        st.markdown('Collect your clients data into your database. Until now, these are the first 10 rows that you have collected so far:')
        st.dataframe(df)