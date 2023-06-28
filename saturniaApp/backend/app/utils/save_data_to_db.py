import pandas as pd
from sqlalchemy import inspect, text

def save_data_to_db(engine, df):
    with engine.connect() as connection:
        print(df.head())
        df.to_sql('recibos', connection, index=True, index_label='recibo', if_exists='append')
        result = connection.execute(text('SELECT * FROM recibos LIMIT 5'))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

        return df
