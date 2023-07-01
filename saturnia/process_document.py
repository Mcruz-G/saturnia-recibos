import os
import json 
from google.cloud import documentai_v1beta3 as documentai


def process_document(file_path: str):

    keys = get_keys()
    mime_type = 'application/pdf'
    project_id, location, processor_id, key_name = keys['project_id'], keys['location'], keys['processor_id'], keys['key_name']
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{os.getcwd()}/keys/{key_name}"
    client = documentai.DocumentProcessorServiceClient()

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    with open(file_path, "rb") as image:
        image_content = image.read()

    document = {"mime_type": mime_type, "content": image_content}

    request = {"name": name, "document": document}

    result = client.process_document(request=request)

    document = result.document
    print("Document processing complete.")
    
    predicted_fields = {}
    i = 1
    for entity in document.entities:
        field_name = entity.type_ 

        if field_name == 'line_item':
            field_name += f"_{i}"
            i += 1

        field_value = entity.mention_text
        predicted_fields[field_name] = field_value

    return predicted_fields


def get_text(anchor, document):
    response = ''
    for segment in anchor.segments:
        start_index = segment.start_index
        end_index = segment.end_index
        response += document.text[start_index:end_index]
    return response.strip()


def get_keys():
    file_path = 'keys/saturnia-recibos-42d2ad3e0669.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

