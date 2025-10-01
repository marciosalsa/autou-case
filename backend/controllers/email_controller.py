"""
Main controller for email classification endpoints.
"""
import os
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename

from backend.models.email_models import EmailClassificationRequest
from backend.services.email_service import EmailClassificationService

class EmailController:
    def __init__(self, email_service: EmailClassificationService, upload_folder: str):
        self.email_service = email_service
        self.upload_folder = upload_folder
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def index(self):
        return render_template('index.html')
    
    def health_check(self):
        return jsonify({'status': 'healthy', 'service': 'AutoU Email Classifier'})
    
    def _validate_content(self, data):
        """Validate content from request data"""
        if not data or 'content' not in data:
            return None, 'Content is required'
        
        content = data['content'].strip()
        if not content:
            return None, 'Content cannot be empty'
        
        return content, None
    
    def _create_classification_request(self, content, source, filename=None):
        """Create classification request object"""
        return EmailClassificationRequest(
            content=content,
            source=source,
            filename=filename
        )
    
    def classify_text(self):
        try:
            data = request.get_json()
            content, error = self._validate_content(data)
            if error:
                return jsonify({'error': error}), 400
            
            # Create and process classification request
            classification_request = self._create_classification_request(content, "text")
            result = self.email_service.classify_email_content(classification_request)
            
            return jsonify(result.to_dict())
            
        except Exception as e:
            return jsonify({'error': f'Error processing text: {str(e)}'}), 500
    
    def upload_file(self):
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file selected'}), 400
            
            file = request.files['file']
            if not file.filename:
                return jsonify({'error': 'No file selected'}), 400
            
            # Process file
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            
            # Process file upload
            upload_result = self.email_service.process_file_upload(file_path, filename)
            
            if not upload_result.success or not upload_result.content:
                return jsonify({'error': upload_result.error or "No content extracted from file"}), 400
            
            # Create and process classification request
            classification_request = self._create_classification_request(
                upload_result.content, "file", filename
            )
            result = self.email_service.classify_email_content(classification_request)
            
            return jsonify(result.to_dict())
                
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    def classify_api(self):
        try:
            # Extract content based on request type
            if request.is_json:
                data = request.get_json()
                content = data.get('content', '').strip()
                filename = data.get('filename')
            else:
                content = request.form.get('content', '').strip()
                filename = request.form.get('filename')
            
            if not content:
                return jsonify({'error': 'Content is required'}), 400
            
            # Create and process classification request
            classification_request = self._create_classification_request(content, "api", filename)
            result = self.email_service.classify_email_content(classification_request)
            
            return jsonify(result.to_dict())
            
        except Exception as e:
            return jsonify({'error': f'Classification error: {str(e)}'}), 500