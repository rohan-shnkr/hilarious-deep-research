"""
Web search tool for gathering articles and information
"""
import os
import aiohttp
import asyncio
from typing import Dict, List, Any
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class WebSearchTool:
    """Tool for searching the web and extracting article content"""
    
    def __init__(self):
        self.serp_api_key = os.getenv("SERP_API_KEY")
        self.session = None
    
    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def execute(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for articles related to the query
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary containing search results and extracted content
        """
        try:
            # Search using SerpAPI (or fallback to direct search)
            search_results = await self._search_web(query, max_results)
            
            # Extract content from each result
            articles = []
            for result in search_results:
                article_content = await self._extract_article_content(result["url"])
                if article_content:
                    articles.append({
                        "title": result["title"],
                        "url": result["url"],
                        "snippet": result["snippet"],
                        "content": article_content[:2000],  # Limit content length
                        "word_count": len(article_content.split())
                    })
            
            return {
                "query": query,
                "articles": articles,
                "total_found": len(articles)
            }
            
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return {"query": query, "articles": [], "error": str(e)}
    
    async def _search_web(self, query: str, max_results: int) -> List[Dict]:
        """Perform web search using SerpAPI"""
        if not self.serp_api_key:
            # Fallback to a simple search simulation
            return self._simulate_search_results(query, max_results)
        
        session = await self._get_session()
        
        params = {
            "q": query,
            "api_key": self.serp_api_key,
            "engine": "google",
            "num": max_results
        }
        
        async with session.get("https://serpapi.com/search", params=params) as response:
            data = await response.json()
            
            results = []
            for item in data.get("organic_results", [])[:max_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
            
            return results
    
    def _simulate_search_results(self, query: str, max_results: int) -> List[Dict]:
        """Simulate search results when no API key is available"""
        # This is a fallback - in production you'd want real search results
        return [
            {
                "title": f"Article about {query} - Result {i+1}",
                "url": f"https://example.com/article-{i+1}",
                "snippet": f"This is a simulated snippet about {query}. " * 3
            }
            for i in range(max_results)
        ]
    
    async def _extract_article_content(self, url: str) -> str:
        """Extract main content from an article URL"""
        try:
            session = await self._get_session()
            
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; TimUrbanBot/1.0)"
            }
            
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    return ""
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Extract main content (simple heuristic)
                content_selectors = [
                    'article', 
                    '.content', 
                    '.post-content',
                    '.entry-content',
                    'main',
                    '#content'
                ]
                
                content = ""
                for selector in content_selectors:
                    element = soup.select_one(selector)
                    if element:
                        content = element.get_text(strip=True)
                        break
                
                if not content:
                    # Fallback to body text
                    content = soup.get_text(strip=True)
                
                return content
                
        except Exception as e:
            logger.warning(f"Failed to extract content from {url}: {e}")
            return ""
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
