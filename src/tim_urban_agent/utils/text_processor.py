"""
Text processing utilities for content extraction and analysis
"""
import re
from typing import List, Dict, Any
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    """Utility class for processing and analyzing text content"""
    
    @staticmethod
    def extract_key_sentences(text: str, max_sentences: int = 5) -> List[str]:
        """Extract the most important sentences from text"""
        sentences = re.split(r'[.!?]+', text)
        
        # Score sentences by various factors
        scored_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  # Skip very short sentences
                continue
            
            score = 0
            
            # Length scoring (prefer medium length)
            length = len(sentence.split())
            if 10 <= length <= 30:
                score += 2
            elif 5 <= length <= 40:
                score += 1
            
            # Position scoring (earlier sentences often more important)
            position = sentences.index(sentence + '.')
            if position < 3:
                score += 3
            elif position < 10:
                score += 1
            
            # Keyword scoring
            keywords = ['important', 'key', 'main', 'significant', 'crucial', 'essential']
            for keyword in keywords:
                if keyword in sentence.lower():
                    score += 2
            
            scored_sentences.append((score, sentence))
        
        # Sort by score and return top sentences
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        return [sentence for score, sentence in scored_sentences[:max_sentences]]
    
    @staticmethod
    def clean_transcript(transcript: str) -> str:
        """Clean YouTube transcript text"""
        # Remove timestamps
        transcript = re.sub(r'\d+:\d+', '', transcript)
        
        # Remove speaker labels
        transcript = re.sub(r'^[A-Z\s]+:', '', transcript, flags=re.MULTILINE)
        
        # Remove extra whitespace
        transcript = ' '.join(transcript.split())
        
        # Remove common transcript artifacts
        artifacts = ['[Music]', '[Applause]', '[Laughter]', '(inaudible)', '(crosstalk)']
        for artifact in artifacts:
            transcript = transcript.replace(artifact, '')
        
        return transcript.strip()
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return "unknown"
    
    @staticmethod
    def is_academic_source(url: str) -> bool:
        """Check if URL appears to be from an academic source"""
        academic_domains = ['.edu', 'scholar.google', 'arxiv.org', 'pubmed.ncbi']
        return any(domain in url.lower() for domain in academic_domains)    @staticmethod
    def extract_quotes(text: str) -> List[str]:
        """Extract quoted text from content"""
        # Find text in quotes
        quotes = re.findall(r'"([^"]*)"', text)
        quotes.extend(re.findall(r"'([^']*)'", text))
        
        # Filter out short quotes
        meaningful_quotes = [q for q in quotes if len(q.split()) > 5]
        
        return meaningful_quotes[:5]  # Return top 5 quotes
    
    @staticmethod
    def categorize_content(text: str) -> str:
        """Categorize content type based on text analysis"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['study', 'research', 'analysis', 'experiment']):
            return 'research'
        elif any(term in text_lower for term in ['tutorial', 'how to', 'guide', 'step']):
            return 'tutorial'
        elif any(term in text_lower for term in ['opinion', 'think', 'believe', 'perspective']):
            return 'opinion'
        elif any(term in text_lower for term in ['news', 'announced', 'today', 'breaking']):
            return 'news'
        else:
            return 'general'
