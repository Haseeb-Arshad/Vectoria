from manim import *

# 3Blue1Brown Style Palette
COLORS = {
    "background": "#1e1e1e",  # Dark Grey
    "primary_blue": "#58C4DD",
    "primary_yellow": "#FFFF00",
    "text": "#FFFFFF"
}

# Strict Template String for LLM Generation
TEMPLATE_STRING = """
from manim import *

config.background_color = "{background}"

class GenScene(Scene):
    def construct(self):
        # 3Blue1Brown-inspired styles
        Text.set_default(color="{text}")
        MathTex.set_default(color="{text}")
        
        # Primary colors for use in the scene
        BLUE_C = "{primary_blue}"
        YELLOW_C = "{primary_yellow}"

        {content}
"""

def get_filled_template(content: str) -> str:
    return TEMPLATE_STRING.format(
        background=COLORS["background"],
        text=COLORS["text"],
        primary_blue=COLORS["primary_blue"],
        primary_yellow=COLORS["primary_yellow"],
        content=content
    )
