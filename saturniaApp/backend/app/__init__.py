from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = '1234'  # Set a secret key for session security

    from .routes.upload_routes import bp as saturnia_bp
    app.register_blueprint(saturnia_bp)

    return app
