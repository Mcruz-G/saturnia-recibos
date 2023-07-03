from flask import Flask, render_template
from upload_routes import bp as upload  # add this line
from google.cloud import secretmanager
import os, shutil

app = Flask(__name__)
app.secret_key = '123'  # Set a secret key
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'pdfs')
app.register_blueprint(upload)

@app.route('/')
def home():
    #Get absolute path to pdfs
    # pdfs_path = os.path.join(os.getcwd(), 'pdfs')
    # if os.path.exists(pdfs_path):
    #     shutil.rmtree(pdfs_path)
    #     os.mkdir(pdfs_path)

    return render_template('index.html')

if __name__ == '__main__':

    app.run(port='8080', host='0.0.0.0')
