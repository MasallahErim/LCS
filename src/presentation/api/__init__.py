### File: src/presentation/api/__init__.py
from flask import Flask
from src.presentation.api.routes import comment_bp

def create_app():
    app = Flask(__name__)
    # Load config
    from config import settings
    app.config['API_HOST'] = settings.api_host
    app.config['API_PORT'] = settings.api_port

    # Register blueprints
    app.register_blueprint(comment_bp, url_prefix='/comments')
    return app