"""
AutoU Email Classifier - Main Application
Using modular backend architecture with proper separation of concerns.
"""
import os
import sys
from flask import Flask

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import from our modular backend
from backend.config.settings import get_config
from backend.controllers.email_controller import EmailController
from backend.services.email_service import EmailClassificationService

def create_app():
    """Create and configure Flask application using modular backend"""
    app = Flask(__name__, 
                template_folder='frontend/templates',
                static_folder='frontend/static')
    
    # Load configuration
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Validate configuration
    config_class.validate()
    
    # Initialize services (Dependency Injection)
    email_service = EmailClassificationService(
        openai_api_key=config_class.OPENAI_API_KEY,
        allowed_extensions=config_class.ALLOWED_EXTENSIONS
    )
    
    # Initialize controller
    email_controller = EmailController(
        email_service=email_service,
        upload_folder=config_class.UPLOAD_FOLDER
    )
    
    # Register routes
    app.add_url_rule('/', 'index', email_controller.index, methods=['GET'])
    app.add_url_rule('/health', 'health', email_controller.health_check, methods=['GET'])
    app.add_url_rule('/classify-text', 'classify_text', email_controller.classify_text, methods=['POST'])
    app.add_url_rule('/upload', 'upload', email_controller.upload_file, methods=['POST'])
    app.add_url_rule('/api/classify', 'classify_api', email_controller.classify_api, methods=['POST'])
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    # Create uploads directory
    config_class = get_config()
    os.makedirs(config_class.UPLOAD_FOLDER, exist_ok=True)
    
    # Run application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))