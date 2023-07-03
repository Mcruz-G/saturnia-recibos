from process_and_send_files import save_data_to_bigquery

def save_data_to_db(df, user_id):
    df['user_id'] = user_id
    save_data_to_bigquery(df)

