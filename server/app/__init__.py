from flask import Flask
from flask_cors import CORS
from .db import init_db
from .routes import auth_bp, upload_bp, appointments_bp, admin_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object("app.config.Config")

    # Init DB
    with app.app_context():
        init_db()

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(upload_bp, url_prefix="/upload")
    app.register_blueprint(appointments_bp, url_prefix="/appointments")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
