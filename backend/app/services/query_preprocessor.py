import re

class QueryPreprocessor:
    def __init__(self, max_length: int = 500):
        self.max_length = max_length
        self.allowed_symbols_regex = r'[^\w\s\-/ \.\#\+]'
        
    def _normalize_whitespace(self, text: str) -> str:
        return ' '.join(text.split()).strip()
    
    def _clean_symbols(self, text: str) -> str:
        return re.sub(self.allowed_symbols_regex, '', text)
            
    def _truncate_query(self, text: str) -> str:
        """Truncates the query to a maximum length if necessary."""
        if len(text) > self.max_length:
            return text[:self.max_length]
        return text

    def preprocess(self, raw_query: str) -> str:
        if not raw_query:
            return ""

        processed = self._clean_symbols(raw_query)
        processed = self._normalize_whitespace(processed)
        
        return processed