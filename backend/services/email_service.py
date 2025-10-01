"""
Email classification service - main business logic.
"""
from typing import Optional

from backend.models.email_models import (
    EmailClassificationRequest, 
    EmailClassificationResult, 
    EmailCategory
)
from backend.services.openai_service import OpenAIService
from backend.utils.text_processor import TextPreprocessor
from backend.utils.file_handler import FileProcessor, FileValidator
from backend.models.email_models import FileUploadResult

class EmailClassificationService:
    """Main service for email classification workflow"""
    
    def __init__(self, openai_api_key: str, allowed_extensions: set):
        self.openai_service = OpenAIService(openai_api_key)
        self.text_processor = TextPreprocessor()
        self.file_processor = FileProcessor()
        self.file_validator = FileValidator(allowed_extensions)
    
    def process_file_upload(self, file_path: str, filename: str) -> FileUploadResult:
        """Process uploaded file and extract content"""
        if not self.file_validator.is_allowed_file(filename):
            return FileUploadResult(
                success=False,
                error="File type not allowed. Please upload TXT or PDF files only."
            )
        
        return self.file_processor.process_uploaded_file(file_path, filename)
    
    def classify_email_content(self, request: EmailClassificationRequest) -> EmailClassificationResult:
        """Classify email content and generate response"""
        # Preprocess the text
        preprocessed_content = self.text_processor.preprocess_text(request.content)
        
        # Classify using OpenAI
        classification_result = self.openai_service.classify_email(preprocessed_content)
        
        # Determine category
        category_str = classification_result.get('categoria', 'PRODUTIVO')
        category = EmailCategory.PRODUCTIVE if category_str == 'PRODUTIVO' else EmailCategory.UNPRODUCTIVE
        
        # Generate suggested response
        suggested_response = self.openai_service.generate_response(
            request.content, 
            category_str
        )
        
        # Calculate text statistics
        char_count = len(request.content)
        word_count = len(request.content.split())
        
        return EmailClassificationResult(
            category=category,
            reasoning=classification_result.get('justificativa', 'Classificação automática'),
            suggested_response=suggested_response,
            original_content=request.content,
            char_count=char_count,
            word_count=word_count,
            filename=request.filename
        )