import os
from flask import Flask
from flask_cors import CORS

from .models import db
from config import config


def create_app(config_name=None):
    """Application factory for creating Flask app"""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, supports_credentials=True)
    
    # Create upload folder if not exists
    if not os.path.exists(app.config.get('UPLOAD_FOLDER', 'uploads')):
        os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'))
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.contacts import contacts_bp
    from .routes.import_export import import_export_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(contacts_bp, url_prefix='/api/contacts')
    app.register_blueprint(import_export_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Address Book API is running'}
    
    return app
