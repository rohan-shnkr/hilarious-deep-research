"""
Main Tim Urban Research Agent implementation
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from .tools.web_search_tool import WebSearchTool
from .tools.youtube_tool import YouTubeTool  
from .tools.image_generation_tool import ImageGenerationTool
from .generators.blog_generator import BlogGenerator
from .utils.research_aggregator import ResearchAggregator
from galileo import log, galileo_context

logger = logging.getLogger(__name__)

class TimUrbanResearchAgent:
    """
    Main agent that orchestrates research and blog post generation
    in the style of Tim Urban from Wait But Why
    """
    
    def __init__(self):
        self.web_search = WebSearchTool()
        self.youtube_tool = YouTubeTool()
        self.image_generator = ImageGenerationTool()
        self.blog_generator = BlogGenerator()
        self.research_aggregator = ResearchAggregator()

    @log(span_type="entrypoint", name="tim_urban_research_agent")    
    async def research_topic(
        self,
        topic: str,
        depth: int = 3,
        style: str = "humorous",
        include_cartoons: bool = True
    ) -> Dict[str, Any]:
        """
        Conduct comprehensive research on a topic and generate a Tim Urban-style blog post
        
        Args:
            topic: The topic to research
            depth: Research depth (1-5)
            style: Writing style preference
            include_cartoons: Whether to generate stick figure cartoons
            
        Returns:
            Dictionary containing the blog post and associated media
        """
        logger.info(f"Starting research on topic: {topic}")
        
        try:
            # Phase 1: Initial research gathering
            research_data = await self._gather_research(topic, depth)
            
            # Phase 2: Aggregate and analyze research
            analysis = await self.research_aggregator.analyze_research(research_data, topic)
            
            # Phase 3: Generate blog post structure
            blog_structure = await self.blog_generator.create_structure(analysis, style)
            
            # Phase 4: Generate stick figure cartoons (if requested)
            cartoons = []
            if include_cartoons:
                cartoons = await self._generate_cartoons(blog_structure["cartoon_concepts"])
            
            # Phase 5: Generate final blog post
            blog_post = await self.blog_generator.generate_full_post(
                blog_structure, analysis, cartoons, style
            )
            
            return {
                "blog_post": blog_post,
                "cartoons": cartoons,
                "research_summary": analysis["summary"],
                "sources": research_data["sources"],
                "generated_at": datetime.now().isoformat(),
                "topic": topic,
                "style": style,
                "metrics": {
                    "word_count": len(blog_post.split()),
                    "source_count": len(research_data["sources"]),
                    "cartoon_count": len(cartoons),
                    "research_depth": depth
                }
            }
            
        except Exception as e:
            logger.error(f"Research failed for topic '{topic}': {e}")
            raise
    
    @log(span_type="tool", name="research_gathering")
    async def _gather_research(self, topic: str, depth: int) -> Dict[str, Any]:
        """Gather research from multiple sources"""
        logger.info(f"Gathering research with depth level {depth}")
        
        # Determine search parameters based on depth
        web_results_count = min(depth * 2, 10)
        youtube_results_count = min(depth, 5)
        
        # Execute searches concurrently
        web_task = self.web_search.execute(
            query=topic, 
            max_results=web_results_count
        )
        
        youtube_task = self.youtube_tool.execute(
            query=topic,
            max_videos=youtube_results_count  
        )
        
        # Additional searches for related concepts
        related_searches = await self._generate_related_queries(topic)
        related_tasks = [
            self.web_search.execute(query=query, max_results=2)
            for query in related_searches[:depth]
        ]
        
        # Wait for all searches to complete
        web_results, youtube_results, *related_results = await asyncio.gather(
            web_task, youtube_task, *related_tasks
        )
        
        return {
            "primary_web": web_results,
            "youtube": youtube_results,
            "related": related_results,
            "sources": self._compile_sources(web_results, youtube_results, related_results),
            "depth": depth
        }
    
    # @log(span_type="tool", name="generate_related_queries")
    async def _generate_related_queries(self, topic: str) -> List[str]:
        """Generate related search queries to explore the topic more thoroughly"""
        # This would use an LLM to generate related queries
        # For now, return some basic variations
        return [
            f"{topic} explained simply",
            f"{topic} examples",
            f"{topic} problems and solutions",
            f"future of {topic}",
            f"{topic} vs alternatives"
        ]
    
    # @log(span_type="tool", name="compile_sources")
    def _compile_sources(self, web_results: Dict, youtube_results: Dict, related_results: List) -> List[Dict]:
        """Compile all sources into a structured list"""
        sources = []
        
        # Add web sources
        for article in web_results.get("articles", []):
            sources.append({
                "type": "web",
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "snippet": article.get("snippet", "")
            })
        
        # Add YouTube sources  
        for video in youtube_results.get("videos", []):
            sources.append({
                "type": "youtube",
                "title": video.get("title", ""),
                "url": video.get("url", ""),
                "transcript_preview": video.get("transcript", "")[:200] + "..."
            })
        
        # Add related sources
        for result_set in related_results:
            for article in result_set.get("articles", []):
                sources.append({
                    "type": "related_web",
                    "title": article.get("title", ""),
                    "url": article.get("url", ""),
                    "snippet": article.get("snippet", "")
                })
        
        return sources
    
    @log(span_type="llm", name="generate_cartoons")
    async def _generate_cartoons(self, cartoon_concepts: List[str]) -> List[Dict]:
        """Generate stick figure cartoons for the blog post"""
        cartoons = []
        
        for concept in cartoon_concepts:
            try:
                cartoon_data = await self.image_generator.execute(
                    concept=concept,
                    # style="simple"
                    style="detailed"
                )
                cartoons.append({
                    "concept": concept,
                    "data": cartoon_data["image_data"],
                    "description": cartoon_data.get("description", concept)
                })
            except Exception as e:
                logger.warning(f"Failed to generate cartoon for '{concept}': {e}")
        
        return cartoons
