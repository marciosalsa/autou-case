import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import List

# Download NLTK resources once at module level
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('portuguese'))
        self.whitespace_pattern = re.compile(r'\s+')
        self.punctuation_set = set(string.punctuation)
    
    def tokenize_and_filter(self, text: str) -> List[str]:
        tokens = word_tokenize(text)
        
        return [
            token for token in tokens 
            if (token not in self.punctuation_set and 
                token not in self.stop_words and 
                len(token) > 2)
        ]
    
    def preprocess_text(self, text: str) -> str:
        text = self.whitespace_pattern.sub(' ', text.lower().strip())
        filtered_tokens = self.tokenize_and_filter(text)
        return ' '.join(filtered_tokens)