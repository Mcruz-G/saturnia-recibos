import pandas as pd
from sqlalchemy import inspect, text

def save_data_to_db(engine, df):
    with engine.connect() as connection:
        print(df.head())
        df.to_sql('recibos', connection, index=True, index_label='recibo', if_exists='append')
        return df
