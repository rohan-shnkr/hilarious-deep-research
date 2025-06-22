"""
MCP Server implementation for Tim Urban Research Agent
"""
import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from .agent import TimUrbanResearchAgent
from .tools.web_search_tool import WebSearchTool
from .tools.youtube_tool import YouTubeTool
from .tools.image_generation_tool import ImageGenerationTool

logger = logging.getLogger(__name__)

class TimUrbanMCPServer:
    """MCP Server for Tim Urban Research Agent"""
    
    def __init__(self):
        self.server = Server("tim-urban-research-agent")
        self.agent = TimUrbanResearchAgent()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up MCP server handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="research_topic",
                    description="Conduct deep research on a topic and generate a Tim Urban-style blog post with cartoons",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "The topic to research (e.g., 'How Neural Networks Work', 'The Future of Space Travel')"
                            },
                            "depth": {
                                "type": "integer", 
                                "description": "Research depth level (1-5, default: 3)",
                                "default": 3,
                                "minimum": 1,
                                "maximum": 5
                            },
                            "style": {
                                "type": "string",
                                "description": "Writing style preference",
                                "enum": ["humorous", "technical", "balanced"],
                                "default": "humorous"
                            },
                            "include_cartoons": {
                                "type": "boolean",
                                "description": "Whether to generate stick figure cartoons",
                                "default": True
                            }
                        },
                        "required": ["topic"]
                    }
                ),
                Tool(
                    name="web_search",
                    description="Search the web for articles and information",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "query": {"type": "string", "description": "Search query"},
                            "max_results": {"type": "integer", "default": 5}
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="youtube_search",
                    description="Search YouTube and extract video transcripts",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "YouTube search query"},
                            "max_videos": {"type": "integer", "default": 3}
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="generate_cartoon",
                    description="Generate a Tim Urban-style stick figure cartoon",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "concept": {"type": "string", "description": "Concept to illustrate"},
                            "style": {"type": "string", "enum": ["simple", "detailed"], "default": "simple"}
                        },
                        "required": ["concept"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls"""
            try:
                if name == "research_topic":
                    result = await self.agent.research_topic(**arguments)
                    return CallToolResult(
                        content=[
                            TextContent(
                                type="text",
                                text=result["blog_post"]
                            )
                        ] + [
                            ImageContent(
                                type="image",
                                data=cartoon["data"],
                                mimeType="image/png"
                            ) for cartoon in result.get("cartoons", [])
                        ]
                    )
                
                elif name == "web_search":
                    web_tool = WebSearchTool()
                    results = await web_tool.execute(**arguments)
                    return CallToolResult(
                        content=[TextContent(type="text", text=json.dumps(results, indent=2))]
                    )
                
                elif name == "youtube_search":
                    youtube_tool = YouTubeTool()
                    results = await youtube_tool.execute(**arguments)
                    return CallToolResult(
                        content=[TextContent(type="text", text=json.dumps(results, indent=2))]
                    )
                
                elif name == "generate_cartoon":
                    image_tool = ImageGenerationTool()
                    result = await image_tool.execute(**arguments)
                    return CallToolResult(
                        content=[
                            ImageContent(
                                type="image",
                                data=result["image_data"],
                                mimeType="image/png"
                            )
                        ]
                    )
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                logger.error(f"Tool execution failed: {e}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )

async def main():
    """Main entry point for the MCP server"""
    server_instance = TimUrbanMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="tim-urban-research-agent",
                server_version="0.1.0",
                capabilities=server_instance.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
