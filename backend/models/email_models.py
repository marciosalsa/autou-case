"""
Email classification models and data structures.
"""
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class EmailCategory(Enum):
    """Email classification categories"""
    PRODUCTIVE = "PRODUTIVO"
    UNPRODUCTIVE = "IMPRODUTIVO"

@dataclass
class EmailClassificationRequest:
    """Request model for email classification"""
    content: str
    source: str = "text"  # "text" or "file"
    filename: Optional[str] = None

@dataclass
class EmailClassificationResult:
    """Result model for email classification"""
    category: EmailCategory
    reasoning: str
    suggested_response: str
    original_content: str
    char_count: int = 0
    word_count: int = 0
    filename: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response"""
        return {
            'category': self.category.value,
            'reasoning': self.reasoning,
            'suggested_response': self.suggested_response,
            'original_content': self.original_content,
            'char_count': self.char_count,
            'word_count': self.word_count,
            'filename': self.filename
        }

@dataclass
class FileUploadResult:
    """Result model for file upload processing"""
    success: bool
    content: Optional[str] = None
    filename: Optional[str] = None
    error: Optional[str] = None