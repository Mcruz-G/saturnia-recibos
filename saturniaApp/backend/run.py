from flask import Flask, render_template
from app.routes.upload_routes import bp as saturnia_bp

app = Flask(__name__, static_folder='images')
app.secret_key = '1234' # This is the line you should add


# Register the Saturnia blueprint
app.register_blueprint(saturnia_bp)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=False)