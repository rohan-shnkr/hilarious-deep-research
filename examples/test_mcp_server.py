#!/usr/bin/env python3
"""
Test script for MCP Server functionality
Demonstrates how the same application flow works through the MCP server architecture
"""
import asyncio
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tim_urban_agent.server import TimUrbanMCPServer

async def test_mcp_server():
    """Test the MCP server functionality"""
    print("🔬 Testing MCP Server Flow\n")
    
    # Initialize the MCP server
    mcp_server = TimUrbanMCPServer()
    
    # Test topic
    test_topic = "How Neural Networks Work"
    
    print("="*60)
    print("MCP SERVER FLOW TEST")
    print("="*60)
    
    try:
        # Step 1: List available tools
        print("\n1️⃣ Listing MCP tools:")
        tools = await mcp_server.server._handlers["list_tools"]()
        for tool in tools:
            print(f"   • {tool.name}: {tool.description}")
        
        # Step 2: Test individual tool calls
        print(f"\n2️⃣ Testing individual MCP tools:")
        
        # Test web search
        print(f"   📡 Testing web_search tool...")
        web_result = await mcp_server.server._handlers["call_tool"](
            name="web_search",
            arguments={"query": test_topic, "max_results": 2}
        )
        print(f"   ✅ Web search: {len(web_result.content)} results")
        
        # Test YouTube search
        print(f"   🎥 Testing youtube_search tool...")
        youtube_result = await mcp_server.server._handlers["call_tool"](
            name="youtube_search",
            arguments={"query": test_topic, "max_videos": 1}
        )
        print(f"   ✅ YouTube search: {len(youtube_result.content)} results")
        
        # Test cartoon generation
        print(f"   🎨 Testing generate_cartoon tool...")
        cartoon_result = await mcp_server.server._handlers["call_tool"](
            name="generate_cartoon",
            arguments={"concept": f"Understanding {test_topic}", "style": "simple"}
        )
        print(f"   ✅ Cartoon generation: {len(cartoon_result.content)} images")
        
        # Step 3: Test full research workflow
        print(f"\n3️⃣ Testing full research_topic workflow:")
        research_result = await mcp_server.server._handlers["call_tool"](
            name="research_topic",
            arguments={
                "topic": test_topic,
                "depth": 2,
                "style": "humorous",
                "include_cartoons": True
            }
        )
        
        # Extract and display results
        blog_post = ""
        cartoons = []
        
        for content in research_result.content:
            if hasattr(content, 'type'):
                if content.type == "text":
                    blog_post = content.text
                elif content.type == "image":
                    cartoons.append({
                        "data": content.data,
                        "mimeType": content.mimeType
                    })
        
        print(f"   ✅ Full research workflow completed!")
        print(f"   📝 Blog post length: {len(blog_post.split())} words")
        print(f"   🎨 Cartoons generated: {len(cartoons)}")
        
        # Display blog post preview
        print(f"\n📄 Blog Post Preview (via MCP Server):")
        print("-" * 40)
        print(blog_post[:500] + "..." if len(blog_post) > 500 else blog_post)
        
        print(f"\n✅ MCP Server test completed successfully!")
        print(f"🎯 This demonstrates the same functionality as run_research.py")
        print(f"   but executed through the MCP server architecture.")
        
    except Exception as e:
        print(f"\n❌ Error during MCP server test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 