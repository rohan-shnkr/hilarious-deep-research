# Tim Urban Research Agent 🤓

An AI-powered research agent that creates hilarious, educational blog posts in the style of Tim Urban from [Wait But Why](https://waitbutwhy.com/), complete with stick figure cartoons to explain complex topics.

## 🎯 What It Does

Give it any topic, and this agent will:

1. **Research deeply** using web search and YouTube videos
2. **Analyze and synthesize** information from multiple sources  
3. **Generate a Tim Urban-style blog post** with humor, analogies, and "aha!" moments
4. **Create stick figure cartoons** to illustrate key concepts
5. **Deliver everything** as a complete, engaging article

## 🏗️ Built With

- **MCP (Model Context Protocol)** - Anthropic's framework for AI tool integration
- **Anthropic Claude** - For generating witty, educational content
- **Web Search APIs** - For gathering research materials
- **YouTube Data API** - For finding and extracting video content  
- **OpenAI DALL-E** - For generating detailed cartoons
- **Matplotlib** - For simple stick figure generation

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- API keys for:
  - Anthropic (for content generation)
  - OpenAI (for image generation)
  - YouTube Data API (for video research)
  - SerpAPI (for web search)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/tim-urban-research-agent.git
   cd tim-urban-research-agent
   ```

2. **Set up environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API keys:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run an example:**
   ```bash
   python examples/run_research.py
   ```

### Usage as MCP Server

```bash
# Start the MCP server
python -m tim_urban_agent.server

# Or use the installed command
tim-urban-agent
```

Then connect from any MCP-compatible client!

## 📚 Usage Examples

### Command Line Interface

```python
from tim_urban_agent import TimUrbanResearchAgent

agent = TimUrbanResearchAgent()

result = await agent.research_topic(
    topic="How Neural Networks Work",
    depth=3,                    # Research depth (1-5)
    style="humorous",          # humorous/technical/balanced  
    include_cartoons=True      # Generate stick figures
)

print(result["blog_post"])
```

### MCP Tool Usage

```json
{
  "name": "research_topic",
  "arguments": {
    "topic": "The Future of Space Travel",
    "depth": 4,
    "style": "balanced",
    "include_cartoons": true
  }
}
```

## 🎨 What You Get

### Tim Urban-Style Blog Post
- **Engaging hook** that draws readers in
- **Step-by-step explanations** of complex concepts
- **Hilarious analogies** and thought experiments
- **"Wait but why" moments** that blow minds
- **Satisfying conclusion** that ties everything together

### Stick Figure Cartoons
- **Simple illustrations** that clarify concepts
- **Hand-drawn aesthetic** matching Tim Urban's style
- **Educational but funny** visual explanations
- **Integrated seamlessly** into the blog post

### Comprehensive Research
- **Multiple web sources** analyzed and synthesized
- **YouTube video transcripts** for diverse perspectives
- **Academic papers** when available
- **Source citations** for credibility

## 🛠️ Architecture

```
Tim Urban Research Agent
├── MCP Server (server.py)
├── Main Agent (agent.py)
├── Research Tools/
│   ├── Web Search Tool
│   ├── YouTube Tool  
│   └── Image Generation Tool
├── Content Generators/
│   ├── Blog Generator
│   └── Cartoon Generator
└── Utilities/
    ├── Research Aggregator
    └── Text Processor
```

## 🔧 Configuration

Key environment variables:

```env
# Required API Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  
YOUTUBE_API_KEY=your_key_here
SERP_API_KEY=your_key_here

# Agent Settings
MAX_RESEARCH_DEPTH=5
MAX_YOUTUBE_VIDEOS=3
MAX_WEB_ARTICLES=5
BLOG_POST_MIN_LENGTH=2000
CARTOON_COUNT=3

# Image Generation
DALLE_MODEL=dall-e-3
DALLE_SIZE=1024x1024
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with coverage
pytest --cov=tim_urban_agent
```

## 📖 Examples

Check out `examples/` for:
- **Interactive research runner** (`run_research.py`)
- **Sample topics** by category (`sample_topics.py`)
- **Jupyter notebooks** with detailed walkthroughs

## 🤝 Contributing

We'd love your help making this agent even better!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Tim Urban** and Wait But Why for inspiring this project
- **Anthropic** for the MCP framework and Claude
- **OpenAI** for DALL-E image generation
- **The research community** for making knowledge accessible

---

*Made with ❤️ and way too much coffee*

**Ready to explain the universe with stick figures? Let's go! 🚀**
