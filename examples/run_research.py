#!/usr/bin/env python3
"""
Example script for running the Tim Urban Research Agent
"""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tim_urban_agent.agent import TimUrbanResearchAgent

async def main():
    """Main example function"""
    # Initialize the agent
    agent = TimUrbanResearchAgent()
    
    # Example topics to research
    topics = [
        "How Neural Networks Actually Work",
        "The Future of Quantum Computing", 
        "Why Consciousness is Weird",
        "The Economics of Space Travel",
        "How Social Media Algorithms Shape Reality"
    ]
    
    # Let user choose a topic or enter their own
    print("🔬 Tim Urban Research Agent - Example Runner\n")
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
        
        print(f"\n🚀 Starting research with depth {depth}, {style} style...")
        print("This may take a few minutes...\n")
        
        # Conduct the research
        result = await agent.research_topic(
            topic=selected_topic,
            depth=depth,
            style=style,
            include_cartoons=include_cartoons
        )
        
        # Save results
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Save blog post
        blog_filename = f"blog_post_{selected_topic.replace(' ', '_').lower()}.md"
        blog_path = output_dir / blog_filename
        
        with open(blog_path, 'w', encoding='utf-8') as f:
            f.write(result["blog_post"])
        
        # Save metadata
        metadata = {
            "topic": result["topic"],
            "style": result["style"],
            "generated_at": result["generated_at"],
            "research_summary": result["research_summary"],
            "sources": result["sources"]
        }
        
        metadata_path = output_dir / f"metadata_{selected_topic.replace(' ', '_').lower()}.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        # Save cartoons if generated
        if result.get("cartoons"):
            import base64
            for i, cartoon in enumerate(result["cartoons"]):
                cartoon_filename = f"cartoon_{i+1}_{selected_topic.replace(' ', '_').lower()}.png"
                cartoon_path = output_dir / cartoon_filename
                
                # Decode base64 and save
                image_data = base64.b64decode(cartoon["data"])
                with open(cartoon_path, 'wb') as f:
                    f.write(image_data)
        
        # Display results
        print("✅ Research complete!\n")
        print(f"📝 Blog post saved to: {blog_path}")
        print(f"📊 Metadata saved to: {metadata_path}")
        
        if result.get("cartoons"):
            print(f"🎨 {len(result['cartoons'])} cartoons saved to output/ directory")
        
        print(f"\n📈 Research Summary:")
        print(f"  • Sources analyzed: {len(result['sources'])}")
        print(f"  • Blog post length: {len(result['blog_post'].split())} words")
        print(f"  • Generated cartoons: {len(result.get('cartoons', []))}")
        
        print("\n" + "="*60)
        print("BLOG POST PREVIEW:")
        print("="*60)
        print(result["blog_post"][:1000] + "..." if len(result["blog_post"]) > 1000 else result["blog_post"])
        
    except KeyboardInterrupt:
        print("\n\n👋 Research interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error during research: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
