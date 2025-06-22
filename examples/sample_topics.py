"""
Sample topics for testing the Tim Urban Research Agent
"""

SAMPLE_TOPICS = {
    "technology": [
        "How Large Language Models Actually Work",
        "The Future of Quantum Computing",
        "Why Blockchain is Either Revolutionary or Overrated",
        "How Your Brain is Like a Computer (And How It's Not)",
        "The Reality of Artificial General Intelligence"
    ],
    
    "science": [
        "Why Consciousness is the Weirdest Thing in the Universe",
        "How Evolution Accidentally Created Intelligence", 
        "The Fermi Paradox: Where is Everybody?",
        "Why Time Travel Breaks Your Brain",
        "How We Know What We Know About Black Holes"
    ],
    
    "society": [
        "How Social Media Algorithms Shape Reality",
        "The Economics of Attention in the Digital Age",
        "Why Democracy is Harder Than It Looks",
        "The Psychology of Conspiracy Theories",
        "How Cities Actually Work (Spoiler: It's Complicated)"
    ],
    
    "future": [
        "The Economics of Space Colonization",
        "How Climate Change Will Reshape Civilization",
        "The Future of Work When AI Does Everything",
        "Why Immortality Might Be a Bad Idea",
        "How Virtual Reality Will Change Human Experience"
    ],
    
    "mind_bending": [
        "What If We're Living in a Simulation?",
        "The Multiverse: Infinite Versions of You",
        "How Mathematics Might Be the Language of Reality",
        "Why Free Will is an Illusion (Or Is It?)",
        "The Universe Might Be Thinking"
    ]
}

def get_random_topic(category=None):
    """Get a random topic, optionally from a specific category"""
    import random
    
    if category and category in SAMPLE_TOPICS:
        return random.choice(SAMPLE_TOPICS[category])
    else:
        all_topics = [topic for topics in SAMPLE_TOPICS.values() for topic in topics]
        return random.choice(all_topics)

def get_topic_by_difficulty():
    """Get topics organized by difficulty level"""
    return {
        "beginner": [
            "How the Internet Actually Works",
            "Why Vaccines Work (The Science Made Simple)",
            "The Basics of How Your Brain Works"
        ],
        "intermediate": [
            "How Machine Learning Actually Works",
            "The Economics of Climate Change",
            "Why Quantum Physics is Weird But Important"
        ],
        "advanced": [
            "The Mathematics of Consciousness",
            "How Complexity Emerges from Simplicity",
            "The Information Theory of Life"
        ]
    }

if __name__ == "__main__":
    print("Sample Topics for Tim Urban Research Agent:")
    print("=" * 50)
    
    for category, topics in SAMPLE_TOPICS.items():
        print(f"\n{category.upper()}:")
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic}")
    
    print(f"\nRandom topic: {get_random_topic()}")
