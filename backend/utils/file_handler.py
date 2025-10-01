import os
from typing import Set
import PyPDF2
from backend.models.email_models import FileUploadResult

class FileValidator:
    def __init__(self, allowed_extensions: Set[str]):
        self.allowed_extensions = allowed_extensions
    
    def is_allowed_file(self, filename: str) -> bool:
        return ('.' in filename and 
                filename.rsplit('.', 1)[1].lower() in self.allowed_extensions)

class FileProcessor:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return ''.join(page.extract_text() for page in pdf_reader.pages).strip()
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read().strip()
    
    def process_uploaded_file(self, file_path: str, filename: str) -> FileUploadResult:
        try:
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            # Extract content based on file type
            content = (
                self.extract_text_from_pdf(file_path) if file_extension == 'pdf'
                else self.extract_text_from_txt(file_path) if file_extension == 'txt'
                else None
            )
            
            if content is None:
                return FileUploadResult(success=False, error=f"Unsupported file type: {file_extension}")
            
            if not content:
                return FileUploadResult(success=False, error="No text content found in the file.")
            
            return FileUploadResult(success=True, content=content, filename=filename)
            
        except Exception as e:
            return FileUploadResult(success=False, error=str(e))
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)