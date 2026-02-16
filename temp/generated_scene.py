
from manim import *

config.background_color = "#1e1e1e"

class GenScene(Scene):
    def construct(self):
        # 3Blue1Brown-inspired styles
        Text.set_default(color="#FFFFFF")
        MathTex.set_default(color="#FFFFFF")
        
        # Primary colors for use in the scene
        BLUE_C = "#58C4DD"
        YELLOW_C = "#FFFF00"

        square = Square(color=BLUE_C, fill_opacity=0.5)
        circle = Circle(color=YELLOW_C, fill_opacity=0.5)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
