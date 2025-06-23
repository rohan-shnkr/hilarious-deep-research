"""
Image generation tool for creating Tim Urban-style stick figure cartoons
"""
import os
import base64
import io
from typing import Dict, Any
from openai import OpenAI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch
import numpy as np
import logging
from galileo import log

logger = logging.getLogger(__name__)

class ImageGenerationTool:
    """Tool for generating Tim Urban-style stick figure cartoons"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.dalle_model = os.getenv("DALLE_MODEL", "dall-e-3")
    
    @log(span_type="tool", name="generate_image")
    async def execute(self, concept: str, style: str = "simple") -> Dict[str, Any]:
        """
        Generate a stick figure cartoon illustrating a concept
        
        Args:
            concept: The concept to illustrate
            style: Style preference ("simple" or "detailed")
            
        Returns:
            Dictionary containing image data and metadata
        """
        try:
            if style == "simple":
                # Generate using matplotlib for simple stick figures
                image_data = await self._generate_simple_cartoon(concept)
                method = "matplotlib"
            else:
                # Generate using DALL-E for more detailed cartoons
                image_data = await self._generate_dalle_cartoon(concept)
                method = "dalle"
            
            return {
                "concept": concept,
                "style": style,
                "image_data": image_data,
                "method": method,
                "description": f"Stick figure cartoon illustrating: {concept}"
            }
            
        except Exception as e:
            logger.error(f"Image generation failed for concept '{concept}': {e}")
            # Return a placeholder image
            placeholder_data = await self._generate_placeholder_cartoon(concept)
            return {
                "concept": concept,
                "style": style,
                "image_data": placeholder_data,
                "method": "placeholder",
                "description": f"Placeholder cartoon for: {concept}",
                "error": str(e)
            }
    
    async def _generate_simple_cartoon(self, concept: str) -> str:
        """Generate a simple stick figure cartoon using matplotlib"""
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        
        # Remove axes
        ax.axis('off')
        
        # Draw stick figure
        self._draw_stick_figure(ax, 3, 2, scale=1.0)
        
        # Add thought bubble with concept
        self._draw_thought_bubble(ax, 6, 5, concept)
        
        # Add title
        ax.text(5, 7.5, f"Understanding: {concept}", 
                ha='center', va='center', fontsize=14, weight='bold')
        
        # Convert to base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        image_data = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return image_data
    
    def _draw_stick_figure(self, ax, x, y, scale=1.0):
        """Draw a simple stick figure"""
        s = scale
        
        # Head
        head = Circle((x, y + 1.5*s), 0.3*s, fill=False, linewidth=2)
        ax.add_patch(head)
        
        # Body
        ax.plot([x, x], [y + 1.2*s, y + 0.3*s], 'k-', linewidth=2)
        
        # Arms
        ax.plot([x - 0.5*s, x + 0.5*s], [y + 0.8*s, y + 0.8*s], 'k-', linewidth=2)
        
        # Legs
        ax.plot([x, x - 0.3*s], [y + 0.3*s, y - 0.5*s], 'k-', linewidth=2)
        ax.plot([x, x + 0.3*s], [y + 0.3*s, y - 0.5*s], 'k-', linewidth=2)
        
        # Simple face
        ax.plot([x - 0.1*s, x - 0.1*s], [y + 1.6*s, y + 1.4*s], 'k-', linewidth=1)  # left eye
        ax.plot([x + 0.1*s, x + 0.1*s], [y + 1.6*s, y + 1.4*s], 'k-', linewidth=1)  # right eye
        
        # Smile
        theta = np.linspace(0.3*np.pi, 0.7*np.pi, 20)
        smile_x = x + 0.15*s * np.cos(theta)
        smile_y = y + 1.3*s + 0.15*s * np.sin(theta)
        ax.plot(smile_x, smile_y, 'k-', linewidth=1)
    
    def _draw_thought_bubble(self, ax, x, y, text):
        """Draw a thought bubble with text"""
        # Main bubble
        bubble = FancyBboxPatch(
            (x - 1, y - 0.5), 2, 1,
            boxstyle="round,pad=0.1",
            facecolor='white',
            edgecolor='black',
            linewidth=1
        )
        ax.add_patch(bubble)
        
        # Small bubbles leading to figure
        for i, (bx, by, size) in enumerate([(x - 1.5, y - 1, 0.1), (x - 2, y - 1.5, 0.05)]):
            small_bubble = Circle((bx, by), size, facecolor='white', edgecolor='black')
            ax.add_patch(small_bubble)
        
        # Text in bubble (wrap long text)
        words = text.split()
        if len(' '.join(words)) > 20:
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            ax.text(x, y + 0.1, line1, ha='center', va='center', fontsize=8, weight='bold')
            ax.text(x, y - 0.1, line2, ha='center', va='center', fontsize=8, weight='bold')
        else:
            ax.text(x, y, text, ha='center', va='center', fontsize=10, weight='bold')
    
    @log(span_type="llm", name="generate_dalle_cartoon")
    async def _generate_dalle_cartoon(self, concept: str) -> str:
        """Generate cartoon using DALL-E"""
        prompt = f"""
        Create a simple, humorous stick figure cartoon in the style of Tim Urban from Wait But Why.
        The cartoon should illustrate: {concept}
        
        Style requirements:
        - Simple black line drawings on white background
        - Stick figure characters with round heads
        - Minimal detail but expressive
        - Include thought bubbles or speech bubbles if helpful
        - Clean, hand-drawn aesthetic
        - Educational but funny
        """
        
        response = self.openai_client.images.generate(
            model=self.dalle_model,
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            response_format="b64_json",
            n=1
        )
        
        return response.data[0].b64_json
    
    async def _generate_placeholder_cartoon(self, concept: str) -> str:
        """Generate a simple placeholder cartoon when other methods fail"""
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        
        # Simple placeholder with text
        ax.text(5, 3, f"[Cartoon: {concept}]", 
                ha='center', va='center', fontsize=12, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray'))
        
        ax.text(5, 2, "🤔", ha='center', va='center', fontsize=24)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        image_data = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return image_data
