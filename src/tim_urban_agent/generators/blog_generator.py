"""
Blog post generator for creating Tim Urban-style content
"""
import os
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader
from anthropic import Anthropic
import logging
from galileo import log

from ..config import config

logger = logging.getLogger(__name__)

class BlogGenerator:
    """Generates Tim Urban-style blog posts from research data"""
    
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Set up templates
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.template_env = Environment(loader=FileSystemLoader(template_dir))
    
    @log(span_type="llm", name="create_structure")
    async def create_structure(self, analysis: Dict[str, Any], style: str) -> Dict[str, Any]:
        """Create a structured outline for the blog post"""
        
        system_prompt = """You are Tim Urban from Wait But Why. Create a detailed blog post structure 
        that breaks down complex topics in your signature style: funny, engaging, and educational.
        
        Your response should include:
        1. A catchy title with subtitle
        2. 5-7 main sections with engaging headers
        3. 3 specific concepts that need stick figure cartoons
        4. Opening hook and closing thoughts
        
        Make it humorous but informative, with your typical analogies and thought experiments."""
        
        user_prompt = f"""
        Based on this research analysis about "{analysis['topic']}":
        
        Summary: {analysis['summary']}
        Key Points: {', '.join(analysis.get('key_points', []))}
        Complexity Level: {analysis.get('complexity', 'medium')}
        
        Create a blog post structure in the {style} style.
        """
        
        try:
            message = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.8,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            response_text = message.content[0].text
            
            # Parse the response into structured data
            structure = self._parse_structure_response(response_text, analysis)
            return structure
            
        except Exception as e:
            logger.error(f"Failed to create blog structure: {e}")
            return self._fallback_structure(analysis)
    
    @log(span_type="llm", name="generate_full_post")
    async def generate_full_post(
        self, 
        structure: Dict[str, Any], 
        analysis: Dict[str, Any], 
        cartoons: List[Dict],
        style: str
    ) -> str:
        """Generate the complete blog post"""
        
        system_prompt = """You are Tim Urban from Wait But Why. Write a complete blog post in your 
        signature style: funny, engaging, deeply educational, with lots of analogies and thought experiments.
        
        Characteristics of your writing:
        - Start with an engaging hook
        - Use lots of humor and relatable analogies  
        - Break down complex concepts step by step
        - Include plenty of "wait but why" moments
        - End with bigger picture implications
        - Use casual, conversational tone
        - Include placeholder markers like [CARTOON 1] where visuals should go"""
        
        template = self.template_env.get_template('blog_post.j2')
        
        user_prompt = template.render(
            structure=structure,
            analysis=analysis,
            cartoons=cartoons,
            style=style
        )
        
        try:
            message = self.anthropic.messages.create(
                model=config.ANTHROPIC_MODEL,
                max_tokens=4000,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            blog_post = message.content[0].text
            
            # Insert cartoon placeholders
            blog_post = self._insert_cartoon_markers(blog_post, cartoons)
            
            return blog_post
            
        except Exception as e:
            logger.error(f"Failed to generate blog post: {e}")
            return self._fallback_blog_post(structure, analysis)
    
    def _parse_structure_response(self, response: str, analysis: Dict) -> Dict[str, Any]:
        """Parse the LLM response into structured data"""
        lines = response.split('\n')
        
        structure = {
            "title": "The Ultimate Guide to " + analysis['topic'],
            "subtitle": "A Deep Dive That Will Change How You Think",
            "sections": [],
            "cartoon_concepts": [],
            "opening_hook": "",
            "closing_thoughts": ""
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.lower().startswith('title:'):
                structure["title"] = line[6:].strip()
            elif line.lower().startswith('subtitle:'):
                structure["subtitle"] = line[9:].strip()
            elif line.lower().startswith('cartoon:'):
                structure["cartoon_concepts"].append(line[8:].strip())
            elif line.startswith('#') or line.startswith('Section'):
                if current_section:
                    structure["sections"].append(current_section)
                current_section = {"header": line.strip('# '), "content_outline": ""}
            elif current_section and line:
                current_section["content_outline"] += line + " "
        
        if current_section:
            structure["sections"].append(current_section)
        
        # Ensure we have at least 3 cartoon concepts
        if len(structure["cartoon_concepts"]) < 3:
            structure["cartoon_concepts"].extend([
                f"Visual explanation of {analysis['topic']}",
                f"Common misconceptions about {analysis['topic']}",
                f"Future implications of {analysis['topic']}"
            ])
        
        return structure
    
    def _insert_cartoon_markers(self, blog_post: str, cartoons: List[Dict]) -> str:
        """Insert cartoon markers into the blog post"""
        for i, cartoon in enumerate(cartoons):
            marker = f"[CARTOON {i+1}: {cartoon['concept']}]"
            # Find good places to insert cartoons (after paragraphs)
            paragraphs = blog_post.split('\n\n')
            if i < len(paragraphs):
                insertion_point = len('\n\n'.join(paragraphs[:i+2]))
                blog_post = blog_post[:insertion_point] + f"\n\n{marker}\n\n" + blog_post[insertion_point:]
        
        return blog_post
    
    def _fallback_structure(self, analysis: Dict) -> Dict[str, Any]:
        """Fallback structure when LLM generation fails"""
        return {
            "title": f"Understanding {analysis['topic']}: A Tim Urban Deep Dive",
            "subtitle": "Breaking Down Complex Concepts with Stick Figures and Analogies",
            "sections": [
                {"header": "What Even Is This Thing?", "content_outline": "Basic introduction"},
                {"header": "Why Should You Care?", "content_outline": "Importance and relevance"},
                {"header": "How It Actually Works", "content_outline": "Technical details simplified"},
                {"header": "Common Misconceptions", "content_outline": "What people get wrong"},
                {"header": "The Bigger Picture", "content_outline": "Implications and future"}
            ],
            "cartoon_concepts": [
                f"What {analysis['topic']} looks like to beginners",
                f"How {analysis['topic']} actually works",
                f"The future of {analysis['topic']}"
            ],
            "opening_hook": f"So you want to understand {analysis['topic']}...",
            "closing_thoughts": "And that's the story of how everything connects."
        }
    
    def _fallback_blog_post(self, structure: Dict, analysis: Dict) -> str:
        """Generate a basic fallback blog post"""
        return f"""
# {structure['title']}
## {structure['subtitle']}

{structure.get('opening_hook', 'Let me tell you a story...')}

## Introduction

So here's the thing about {analysis['topic']} - it's one of those concepts that seems simple on the surface but is actually mind-bendingly complex when you dig deeper. Kind of like asking "what is consciousness?" or "why do hot dogs come in packs of 10 but buns come in packs of 8?"

[CARTOON 1: Initial confusion about the topic]

## The Basics

Let me start with what we know...

{analysis.get('summary', 'This is a fascinating topic that deserves deeper exploration.')}

## Going Deeper

Now here's where it gets interesting...

[CARTOON 2: Mind blown realization]

## The Big Picture

When you zoom out and look at the implications...

[CARTOON 3: Future implications]

## Conclusion

And that's the story of {analysis['topic']}. Pretty wild, right?

---

*Sources: Various internet rabbit holes and YouTube videos that may or may not be completely accurate.*
"""
