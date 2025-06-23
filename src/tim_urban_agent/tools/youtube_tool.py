"""
YouTube search and transcript extraction tool
"""
import os
import asyncio
from typing import Dict, List, Any, Optional
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import logging
from galileo import log

# Try to import config, fallback to os.getenv if not available
try:
    from ..config import config
    YOUTUBE_API_KEY = config.YOUTUBE_API_KEY
    MAX_YOUTUBE_VIDEOS = config.MAX_YOUTUBE_VIDEOS
except ImportError:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    MAX_YOUTUBE_VIDEOS = int(os.getenv("MAX_YOUTUBE_VIDEOS", "3"))

logger = logging.getLogger(__name__)

class YouTubeTool:
    """Tool for searching YouTube and extracting video transcripts"""
    
    def __init__(self):
        self.api_key = YOUTUBE_API_KEY
        if self.api_key:
            print(f"Using YouTube API key: {self.api_key}")
            # Initialize YouTube API client
            self.youtube = build("youtube", "v3", developerKey=self.api_key)
        else:
            self.youtube = None
            logger.warning("YouTube API key not found - using simulation mode")
    
    @log(span_type="tool", name="youtube_search")
    async def execute(self, query: str, max_videos: int = 3) -> Dict[str, Any]:
        """
        Search YouTube for videos and extract transcripts
        
        Args:
            query: Search query
            max_videos: Maximum number of videos to process
            
        Returns:
            Dictionary containing video information and transcripts
        """
        try:
            # Search for videos
            video_results = await self._search_videos(query, max_videos)
            
            # Extract transcripts concurrently
            videos_with_transcripts = []
            transcript_tasks = [
                self._get_video_transcript(video["video_id"])
                for video in video_results
            ]
            
            transcripts = await asyncio.gather(*transcript_tasks, return_exceptions=True)
            
            for video, transcript in zip(video_results, transcripts):
                if isinstance(transcript, Exception):
                    transcript_text = f"Transcript not available: {str(transcript)}"
                else:
                    transcript_text = transcript
                
                videos_with_transcripts.append({
                    **video,
                    "transcript": transcript_text,
                    "transcript_length": len(transcript_text.split()) if isinstance(transcript, str) else 0
                })
            
            return {
                "query": query,
                "videos": videos_with_transcripts,
                "total_found": len(videos_with_transcripts)
            }
            
        except Exception as e:
            logger.error(f"YouTube search failed: {e}")
            return {"query": query, "videos": [], "error": str(e)}
    
    @log(span_type="tool", name="search_videos")
    async def _search_videos(self, query: str, max_results: int) -> List[Dict]:
        """Search for YouTube videos"""
        if not self.youtube:
            return self._simulate_video_results(query, max_results)
        
        try:
            search_response = self.youtube.search().list(
                q=query,
                part="snippet",
                maxResults=max_results,
                type="video",
                order="relevance"
            ).execute()
            
            videos = []
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                snippet = item["snippet"]
                
                videos.append({
                    "video_id": video_id,
                    "title": snippet["title"],
                    "description": snippet["description"][:500],
                    "channel": snippet["channelTitle"],
                    "published_at": snippet["publishedAt"],
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "thumbnail": snippet["thumbnails"]["high"]["url"]
                })
            
            return videos
            
        except Exception as e:
            logger.error(f"YouTube API search failed: {e}")
            return self._simulate_video_results(query, max_results)
    
    def _simulate_video_results(self, query: str, max_results: int) -> List[Dict]:
        """Simulate video results when API is not available"""
        return [
            {
                "video_id": f"sim_vid_{i}",
                "title": f"Video about {query} - Part {i+1}",
                "description": f"This is a simulated video description about {query}.",
                "channel": f"Educational Channel {i+1}",
                "published_at": "2024-01-01T00:00:00Z",
                "url": f"https://youtube.com/watch?v=sim_vid_{i}",
                "thumbnail": "https://via.placeholder.com/480x360"
            }
            for i in range(max_results)
        ]
    
    @log(span_type="tool", name="get_video_transcript")
    async def _get_video_transcript(self, video_id: str) -> str:
        """Extract transcript from a YouTube video"""
        try:
            # Try to get transcript in English first
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=['en', 'en-US', 'en-GB']
            )
            
            # Combine all transcript segments
            full_transcript = " ".join([
                segment['text'] for segment in transcript_list
            ])
            
            return full_transcript
            
        except Exception as e:
            # If transcript is not available, return a placeholder
            logger.warning(f"Could not get transcript for video {video_id}: {e}")
            return f"Transcript not available for video {video_id}"
