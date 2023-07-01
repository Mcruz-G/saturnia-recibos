import os
from process_document import process_document
import pandas as pd

def process_and_send_files(file_paths):
    fields = {}
    if isinstance(file_paths, str):
        file_paths = [file_paths]
        
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            name = os.path.basename(file_path).split(".")[0]
            result = process_document(file_path)
            fields[name] = result

    df = pd.DataFrame.from_dict(fields, orient='index')
    return df