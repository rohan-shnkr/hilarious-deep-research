"""
Cartoon generator for creating Tim Urban-style illustrations
"""
import logging

logger = logging.getLogger(__name__)

class CartoonGenerator:
    """Generates cartoon concepts and descriptions for Tim Urban-style illustrations"""
    
    def __init__(self):
        pass
    
    def generate_concepts(self, topic: str, key_points: list) -> list:
        """Generate cartoon concepts based on topic and key points"""
        concepts = []
        
        # Basic concept for the topic itself
        concepts.append(f"Simple visual explanation of {topic}")
        
        # Concepts based on key points
        for i, point in enumerate(key_points[:3]):
            if "how" in point.lower():
                concepts.append(f"Step-by-step breakdown: {point}")
            elif "why" in point.lower():
                concepts.append(f"Thought bubble explanation: {point}")
            else:
                concepts.append(f"Visual metaphor for: {point}")
        
        # Common Tim Urban cartoon themes
        if len(concepts) < 3:
            concepts.extend([
                f"Before and after understanding {topic}",
                f"Common misconceptions about {topic}",
                f"The future implications of {topic}"
            ])
        
        return concepts[:3]  # Return top 3 concepts
    
    def create_description(self, concept: str) -> str:
        """Create a detailed description for a cartoon concept"""
        return f"""
        Stick figure cartoon showing: {concept}
        
        Style: Simple black line drawings on white background
        Characters: Basic stick figures with round heads
        Elements: Thought bubbles, simple objects, minimal text
        Mood: Educational but humorous, in Tim Urban's style
        """
