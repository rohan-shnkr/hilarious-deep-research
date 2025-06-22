"""
Test cases for Tim Urban Agent tools
"""
import pytest
import asyncio
import os
from unittest.mock import Mock, patch

from tim_urban_agent.tools.web_search_tool import WebSearchTool
from tim_urban_agent.tools.youtube_tool import YouTubeTool
from tim_urban_agent.tools.image_generation_tool import ImageGenerationTool

class TestWebSearchTool:
    """Test cases for WebSearchTool"""
    
    @pytest.mark.asyncio
    async def test_web_search_basic(self):
        """Test basic web search functionality"""
        tool = WebSearchTool()
        
        result = await tool.execute("artificial intelligence", max_results=3)
        
        assert "query" in result
        assert "articles" in result
        assert result["query"] == "artificial intelligence"
        
        # Clean up
        await tool.close()
    
    @pytest.mark.asyncio
    async def test_web_search_with_content_extraction(self):
        """Test web search with content extraction"""
        tool = WebSearchTool()
        
        with patch.object(tool, '_extract_article_content') as mock_extract:
            mock_extract.return_value = "Sample article content for testing."
            
            result = await tool.execute("machine learning", max_results=2)
            
            assert len(result["articles"]) <= 2
            for article in result["articles"]:
                assert "title" in article
                assert "url" in article
                assert "content" in article
        
        await tool.close()

class TestYouTubeTool:
    """Test cases for YouTubeTool"""
    
    @pytest.mark.asyncio
    async def test_youtube_search_basic(self):
        """Test basic YouTube search"""
        tool = YouTubeTool()
        
        result = await tool.execute("neural networks explained", max_videos=2)
        
        assert "query" in result
        assert "videos" in result
        assert result["query"] == "neural networks explained"
        assert len(result["videos"]) <= 2
    
    @pytest.mark.asyncio
    async def test_youtube_transcript_extraction(self):
        """Test transcript extraction functionality"""
        tool = YouTubeTool()
        
        # Test with a known video ID (mock)
        with patch.object(tool, '_get_video_transcript') as mock_transcript:
            mock_transcript.return_value = "This is a sample transcript for testing."
            
            transcript = await tool._get_video_transcript("test_video_id")
            assert transcript == "This is a sample transcript for testing."

class TestImageGenerationTool:
    """Test cases for ImageGenerationTool"""
    
    @pytest.mark.asyncio
    async def test_simple_cartoon_generation(self):
        """Test simple cartoon generation"""
        tool = ImageGenerationTool()
        
        result = await tool.execute("How computers think", style="simple")
        
        assert "concept" in result
        assert "image_data" in result
        assert "method" in result
        assert result["concept"] == "How computers think"
    
    @pytest.mark.asyncio
    async def test_dalle_cartoon_generation(self):
        """Test DALL-E cartoon generation"""
        tool = ImageGenerationTool()
        
        # Mock the OpenAI client
        with patch.object(tool, 'openai_client') as mock_client:
            mock_response = Mock()
            mock_response.data = [Mock()]
            mock_response.data[0].b64_json = "fake_base64_image_data"
            mock_client.images.generate.return_value = mock_response
            
            result = await tool.execute("How the internet works", style="detailed")
            
            assert result["method"] == "dalle"
            assert result["image_data"] == "fake_base64_image_data"

if __name__ == "__main__":
    pytest.main([__file__])
