"""
Research aggregation and analysis utilities
"""
import re
from typing import Dict, List, Any
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class ResearchAggregator:
    """Aggregates and analyzes research data from multiple sources"""
    
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
    
    async def analyze_research(self, research_data: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """
        Analyze all research data and extract key insights
        
        Args:
            research_data: Raw research data from multiple sources
            topic: The research topic
            
        Returns:
            Structured analysis of the research
        """
        try:
            # Extract all text content
            all_text = self._extract_all_text(research_data)
            
            # Analyze content
            key_points = self._extract_key_points(all_text, topic)
            themes = self._identify_themes(all_text)
            complexity_level = self._assess_complexity(all_text)
            source_quality = self._assess_source_quality(research_data)
            
            # Generate summary
            summary = self._generate_summary(all_text, topic, key_points)
            
            # Identify gaps
            potential_gaps = self._identify_research_gaps(key_points, topic)
            
            return {
                "topic": topic,
                "summary": summary,
                "key_points": key_points,
                "themes": themes,
                "complexity": complexity_level,
                "source_quality": source_quality,
                "potential_gaps": potential_gaps,
                "total_sources": self._count_sources(research_data),
                "word_count": len(all_text.split())
            }
            
        except Exception as e:
            logger.error(f"Research analysis failed: {e}")
            return self._fallback_analysis(topic)
    
    def _extract_all_text(self, research_data: Dict[str, Any]) -> str:
        """Extract all text content from research data"""
        all_text = []
        
        # Web articles
        for article in research_data.get("primary_web", {}).get("articles", []):
            all_text.append(article.get("content", ""))
            all_text.append(article.get("snippet", ""))
        
        # YouTube transcripts
        for video in research_data.get("youtube", {}).get("videos", []):
            all_text.append(video.get("transcript", ""))
            all_text.append(video.get("description", ""))
        
        # Related articles
        for result_set in research_data.get("related", []):
            for article in result_set.get("articles", []):
                all_text.append(article.get("content", ""))
                all_text.append(article.get("snippet", ""))
        
        return " ".join(all_text)
    
    def _extract_key_points(self, text: str, topic: str) -> List[str]:
        """Extract key points from the research text"""
        # Simple extraction based on sentence importance
        sentences = re.split(r'[.!?]+', text)
        
        key_points = []
        topic_words = set(topic.lower().split())
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20 or len(sentence) > 200:
                continue
            
            # Score sentence based on topic relevance
            words = set(re.findall(r'\b\w+\b', sentence.lower()))
            topic_overlap = len(words.intersection(topic_words))
            
            # Look for key indicators
            key_indicators = ['important', 'key', 'main', 'primary', 'essential', 
                            'crucial', 'significant', 'major', 'fundamental']
            has_indicators = any(indicator in sentence.lower() for indicator in key_indicators)
            
            if topic_overlap > 0 or has_indicators:
                key_points.append(sentence.strip())
        
        # Return top key points
        return key_points[:8]
    
    def _identify_themes(self, text: str) -> List[str]:
        """Identify major themes in the research"""
        # Extract frequent meaningful words
        words = re.findall(r'\b\w{4,}\b', text.lower())
        word_freq = Counter(word for word in words if word not in self.stop_words)
        
        # Get top themes
        top_words = [word for word, count in word_freq.most_common(10)]
        
        # Group related words into themes
        themes = []
        used_words = set()
        
        for word in top_words:
            if word in used_words:
                continue
            
            # Find related words (simple approach)
            related = [w for w in top_words if w not in used_words and 
                      (w.startswith(word[:4]) or word.startswith(w[:4]))]
            
            if related:
                theme = f"{word} ({', '.join(related[:2])})"
                themes.append(theme)
                used_words.update([word] + related)
            else:
                themes.append(word)
                used_words.add(word)
        
        return themes[:5]
    
    def _assess_complexity(self, text: str) -> str:
        """Assess the complexity level of the topic"""
        # Simple heuristics for complexity
        technical_indicators = [
            'algorithm', 'quantum', 'molecular', 'statistical', 'theoretical',
            'computational', 'mathematical', 'scientific', 'engineering',
            'technical', 'advanced', 'complex', 'sophisticated'
        ]
        
        simple_indicators = [
            'basic', 'simple', 'easy', 'beginner', 'introduction', 'overview',
            'fundamentals', 'basics', 'elementary'
        ]
        
        text_lower = text.lower()
        technical_count = sum(1 for term in technical_indicators if term in text_lower)
        simple_count = sum(1 for term in simple_indicators if term in text_lower)
        
        # Calculate average sentence length
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        if technical_count > simple_count and avg_sentence_length > 20:
            return "high"
        elif simple_count > technical_count and avg_sentence_length < 15:
            return "low"
        else:
            return "medium"
    
    def _assess_source_quality(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality of research sources"""
        quality_indicators = {
            "total_sources": self._count_sources(research_data),
            "has_academic": False,
            "has_video": len(research_data.get("youtube", {}).get("videos", [])) > 0,
            "source_diversity": 0,
            "avg_content_length": 0
        }
        
        # Check for academic sources
        all_urls = []
        content_lengths = []
        
        for article in research_data.get("primary_web", {}).get("articles", []):
            url = article.get("url", "")
            all_urls.append(url)
            content_lengths.append(len(article.get("content", "")))
            
            if any(domain in url for domain in ['.edu', 'scholar.', 'arxiv.', 'pubmed']):
                quality_indicators["has_academic"] = True
        
        # Calculate diversity (unique domains)
        domains = set()
        for url in all_urls:
            try:
                domain = url.split("//")[1].split("/")[0]
                domains.add(domain)
            except:
                pass
        
        quality_indicators["source_diversity"] = len(domains)
        quality_indicators["avg_content_length"] = sum(content_lengths) / max(len(content_lengths), 1)
        
        return quality_indicators
    
    def _generate_summary(self, text: str, topic: str, key_points: List[str]) -> str:
        """Generate a summary of the research"""
        # Simple extractive summary
        first_sentences = []
        sentences = re.split(r'[.!?]+', text)
        
        topic_words = set(topic.lower().split())
        
        for sentence in sentences[:20]:  # Look at first 20 sentences
            sentence = sentence.strip()
            if len(sentence) > 30:
                words = set(re.findall(r'\b\w+\b', sentence.lower()))
                if len(words.intersection(topic_words)) > 0:
                    first_sentences.append(sentence)
                    if len(first_sentences) >= 3:
                        break
        
        summary = " ".join(first_sentences)
        if len(summary) < 100:
            summary = f"Research on {topic} reveals several key insights. " + " ".join(key_points[:2])
        
        return summary[:500] + "..." if len(summary) > 500 else summary
    
    def _identify_research_gaps(self, key_points: List[str], topic: str) -> List[str]:
        """Identify potential gaps in the research"""
        common_gaps = [
            "Historical context and development",
            "Real-world applications and examples", 
            "Limitations and criticisms",
            "Future developments and trends",
            "Comparison with alternatives",
            "Economic or social impact"
        ]
        
        # Check which gaps might exist based on key points
        identified_gaps = []
        key_points_text = " ".join(key_points).lower()
        
        gap_keywords = {
            "Historical context": ["history", "historical", "development", "origin", "invented"],
            "Applications": ["application", "use", "example", "implementation", "practical"],
            "Limitations": ["limitation", "problem", "issue", "disadvantage", "criticism"],
            "Future": ["future", "trend", "development", "next", "upcoming"],
            "Comparison": ["vs", "versus", "compared", "alternative", "different"],
            "Impact": ["impact", "effect", "influence", "economic", "social"]
        }
        
        for gap, keywords in gap_keywords.items():
            if not any(keyword in key_points_text for keyword in keywords):
                identified_gaps.append(gap)
        
        return identified_gaps[:3]  # Return top 3 gaps
    
    def _count_sources(self, research_data: Dict[str, Any]) -> int:
        """Count total number of sources"""
        count = 0
        count += len(research_data.get("primary_web", {}).get("articles", []))
        count += len(research_data.get("youtube", {}).get("videos", []))
        
        for result_set in research_data.get("related", []):
            count += len(result_set.get("articles", []))
        
        return count
    
    def _fallback_analysis(self, topic: str) -> Dict[str, Any]:
        """Fallback analysis when processing fails"""
        return {
            "topic": topic,
            "summary": f"Research analysis for {topic} could not be completed.",
            "key_points": [f"Basic information about {topic}", f"Key concepts in {topic}"],
            "themes": [topic.lower()],
            "complexity": "medium",
            "source_quality": {"total_sources": 0, "has_academic": False},
            "potential_gaps": ["More research needed"],
            "total_sources": 0,
            "word_count": 0
        }
