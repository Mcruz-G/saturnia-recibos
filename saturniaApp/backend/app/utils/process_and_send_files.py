import os
from ..docaiprocess.process_document import process_document
import pandas as pd

def process_and_send_files(directory):
    fields = {}
    files = os.listdir(directory)
    for _, filename in enumerate(files):
        if filename.endswith('.pdf'):
            name = filename.split(".")[0]
            file_path = os.path.join(directory, filename)
            result = process_document(file_path)
            fields[name] = result

    df = pd.DataFrame.from_dict(fields, orient='index')
    return df
