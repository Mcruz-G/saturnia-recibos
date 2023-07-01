from flask import Flask, render_template
from upload_routes import bp as upload  # add this line
from google.cloud import secretmanager
import os

app = Flask(__name__)
app.secret_key = '123'  # Set a secret key

app.register_blueprint(upload)
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
