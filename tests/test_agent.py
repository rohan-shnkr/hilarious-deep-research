"""
Test cases for the main Tim Urban Agent
"""
import pytest
import asyncio
from unittest.mock import Mock, patch

from tim_urban_agent.agent import TimUrbanResearchAgent

class TestTimUrbanResearchAgent:
    """Test cases for the main research agent"""
    
    @pytest.mark.asyncio
    async def test_research_topic_basic(self):
        """Test basic research topic functionality"""
        agent = TimUrbanResearchAgent()
        
        # Mock the tools to avoid actual API calls
        with patch.object(agent, 'web_search') as mock_web, \
             patch.object(agent, 'youtube_tool') as mock_youtube, \
             patch.object(agent, 'blog_generator') as mock_blog:
            
            # Set up mock responses
            mock_web.execute.return_value = {
                "articles": [{"title": "Test Article", "content": "Test content"}]
            }
            mock_youtube.execute.return_value = {
                "videos": [{"title": "Test Video", "transcript": "Test transcript"}]
            }
            mock_blog.create_structure.return_value = {
                "title": "Test Title",
                "sections": [{"header": "Test Section"}],
                "cartoon_concepts": ["Test concept"]
            }
            mock_blog.generate_full_post.return_value = "Test blog post content"
            
            result = await agent.research_topic("artificial intelligence")
            
            assert "blog_post" in result
            assert "topic" in result
            assert result["topic"] == "artificial intelligence"
    
    @pytest.mark.asyncio
    async def test_gather_research(self):
        """Test research gathering functionality"""
        agent = TimUrbanResearchAgent()
        
        with patch.object(agent, 'web_search') as mock_web, \
             patch.object(agent, 'youtube_tool') as mock_youtube:
            
            mock_web.execute.return_value = {"articles": []}
            mock_youtube.execute.return_value = {"videos": []}
            
            result = await agent._gather_research("test topic", depth=2)
            
            assert "primary_web" in result
            assert "youtube" in result
            assert "sources" in result
            assert result["depth"] == 2
    
    @pytest.mark.asyncio
    async def test_generate_related_queries(self):
        """Test related query generation"""
        agent = TimUrbanResearchAgent()
        
        queries = await agent._generate_related_queries("machine learning")
        
        assert isinstance(queries, list)
        assert len(queries) > 0
        assert all("machine learning" in query.lower() for query in queries)

if __name__ == "__main__":
    pytest.main([__file__])
