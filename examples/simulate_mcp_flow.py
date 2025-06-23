#!/usr/bin/env python3
"""
Simulation script for MCP Server flow
This demonstrates how the same application flow works through the MCP server architecture
"""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tim_urban_agent.server import TimUrbanMCPServer

async def simulate_mcp_flow():
    """Simulate the MCP server flow"""
    print("🔬 Tim Urban Research Agent - MCP Server Flow Simulation\n")
    
    # Initialize the MCP server
    mcp_server = TimUrbanMCPServer()
    
    # Example topics to research
    topics = [
        "How Neural Networks Actually Work",
        "The Future of Quantum Computing", 
        "Why Consciousness is Weird",
        "The Economics of Space Travel",
        "How Social Media Algorithms Shape Reality"
    ]
    
    # Let user choose a topic or enter their own
    print("Choose a topic to research:")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic}")
    print(f"{len(topics) + 1}. Enter your own topic")
    
    try:
        choice = input(f"\nEnter your choice (1-{len(topics) + 1}): ").strip()
        
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(topics):
                selected_topic = topics[choice_num - 1]
            elif choice_num == len(topics) + 1:
                selected_topic = input("Enter your topic: ").strip()
            else:
                print("Invalid choice. Using default topic.")
                selected_topic = topics[0]
        else:
            print("Invalid input. Using default topic.")
            selected_topic = topics[0]
        
        # Get research parameters
        print(f"\n📚 Researching: {selected_topic}")
        
        depth = input("Research depth (1-5, default 3): ").strip()
        depth = int(depth) if depth.isdigit() and 1 <= int(depth) <= 5 else 3
        
        style = input("Writing style (humorous/technical/balanced, default humorous): ").strip()
        style = style if style in ['humorous', 'technical', 'balanced'] else 'humorous'
        
        include_cartoons = input("Generate cartoons? (y/n, default y): ").strip().lower()
        include_cartoons = include_cartoons != 'n'
        
        print(f"\n🚀 Starting MCP server flow simulation...")
        print("This demonstrates the same flow as run_research.py but through MCP server architecture\n")
        
        # Simulate MCP tool calls
        print("="*60)
        print("MCP SERVER FLOW SIMULATION")
        print("="*60)
        
        # Step 1: List available tools (MCP protocol)
        print("\n1️⃣ Listing available MCP tools:")
        tools = await mcp_server.server._handlers["list_tools"]()
        for tool in tools:
            print(f"   • {tool.name}: {tool.description}")
        
        # Step 2: Simulate individual tool calls
        print(f"\n2️⃣ Simulating individual MCP tool calls:")
        
        # Web search tool call
        print(f"   📡 Calling web_search tool...")
        web_result = await mcp_server.server._handlers["call_tool"](
            name="web_search",
            arguments={"query": selected_topic, "max_results": 3}
        )
        print(f"   ✅ Web search completed: {len(web_result.content)} results")
        
        # YouTube search tool call
        print(f"   🎥 Calling youtube_search tool...")
        youtube_result = await mcp_server.server._handlers["call_tool"](
            name="youtube_search",
            arguments={"query": selected_topic, "max_videos": 2}
        )
        print(f"   ✅ YouTube search completed: {len(youtube_result.content)} results")
        
        # Cartoon generation tool call
        if include_cartoons:
            print(f"   🎨 Calling generate_cartoon tool...")
            cartoon_result = await mcp_server.server._handlers["call_tool"](
                name="generate_cartoon",
                arguments={"concept": f"Understanding {selected_topic}", "style": "detailed"}
            )
            print(f"   ✅ Cartoon generation completed: {len(cartoon_result.content)} images")
        
        # Step 3: Full research topic tool call (main workflow)
        print(f"\n3️⃣ Calling research_topic tool (full workflow):")
        research_arguments = {
            "topic": selected_topic,
            "depth": depth,
            "style": style,
            "include_cartoons": include_cartoons
        }
        
        print(f"   🔬 Executing full research workflow...")
        result = await mcp_server.server._handlers["call_tool"](
            name="research_topic",
            arguments=research_arguments
        )
        
        # Extract results from MCP response
        blog_post = ""
        cartoons = []
        
        for content in result.content:
            if hasattr(content, 'type'):
                if content.type == "text":
                    blog_post = content.text
                elif content.type == "image":
                    cartoons.append({
                        "data": content.data,
                        "mimeType": content.mimeType
                    })
        
        # Save results (same as run_research.py)
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Save blog post
        blog_filename = f"blog_post_mcp_{selected_topic.replace(' ', '_').lower()}.md"
        blog_path = output_dir / blog_filename
        
        with open(blog_path, 'w', encoding='utf-8') as f:
            f.write(blog_post)
        
        # Save cartoons if generated
        if cartoons:
            import base64
            for i, cartoon in enumerate(cartoons):
                cartoon_filename = f"cartoon_mcp_{i+1}_{selected_topic.replace(' ', '_').lower()}.png"
                cartoon_path = output_dir / cartoon_filename
                
                # Decode base64 and save
                image_data = base64.b64decode(cartoon["data"])
                with open(cartoon_path, 'wb') as f:
                    f.write(image_data)
        
        # Display results
        print("\n✅ MCP Server flow simulation complete!\n")
        print(f"📝 Blog post saved to: {blog_path}")
        
        if cartoons:
            print(f"🎨 {len(cartoons)} cartoons saved to output/ directory")
        
        print(f"\n📈 Results Summary:")
        print(f"  • Blog post length: {len(blog_post.split())} words")
        print(f"  • Generated cartoons: {len(cartoons)}")
        print(f"  • MCP tools used: {len(tools)}")
        
        print("\n" + "="*60)
        print("BLOG POST PREVIEW (via MCP Server):")
        print("="*60)
        print(blog_post[:1000] + "..." if len(blog_post) > 1000 else blog_post)
        
        print(f"\n🎯 Key Difference: This flow went through the MCP server architecture!")
        print(f"   • Tools were called via MCP protocol handlers")
        print(f"   • Responses were formatted as MCP content types")
        print(f"   • Same functionality, different interface layer")
        
    except KeyboardInterrupt:
        print("\n\n👋 MCP simulation interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error during MCP simulation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(simulate_mcp_flow()) 