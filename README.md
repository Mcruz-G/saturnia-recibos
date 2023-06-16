# Saturnia

Saturnia is a Streamlit web application for processing zip files containing PDF files. It processes the images using a custom Python function, stores the results in a SQL database, and allows users to download the results as a CSV file.

## Features

- User-friendly interface for uploading zip files
- Automatic extraction and processing of PDF files from the uploaded zip file
- Results are stored in a SQLite database (named 'CFE_Recibos_DB.sqlite') with the table 'recibos'
- Prevents addition of duplicate entries in the database
- Option to download the results as a CSV file
- Displays the first 10 entries of the 'recibos' table in the database

## How to Run

This project requires Python and the following Python libraries installed:

- Streamlit
- pandas
- SQLAlchemy

However, there are other dependencies required for this project. Ideally, you will create a virtualenv and when it's activated go to this repo's 
directory and run the command:

`pip install -r requirements.txt`

this will install all the required dependencies from the requirements.txt file.

### Steps

1. Clone the repo:
    `git clone https://github.com/your-username/saturnia.git`

2. Navigate to the directory:
    `cd saturnia`

3. Run the Streamlit app:
    `streamlit run saturnia_app.py`

You will see the Streamlit app appear in your web browser.

**Note:** This project contains a `process_document()` function that is a placeholder for the actual PDF processing function. You need to replace this function with your own function to process PDF files.

## Usage

1. Click on 'Browse files' to upload a zip file.
2. Navigate to your zip file and select it.
3. Click 'Open' to upload the file.
4. The application will extract and process the PDF files from the zip file.
5. The results are stored in the 'recibos' table in the SQLite database 'CFE_Recibos_DB.sqlite'.
6. The first 10 entries of the 'recibos' table are displayed.
7. You can download the results as a CSV file by clicking 'Download Results as CSV'.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
