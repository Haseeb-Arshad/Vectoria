import os
from openai import OpenAI
from src.styles import get_filled_template

def generate_manim_code(prompt: str, mock: bool = False) -> str:
    """
    Generates Manim code from a natural language prompt.
    If mock is True, returns a pre-written snippet for testing.
    """
    if mock:
        content = """
        square = Square(color=BLUE_C, fill_opacity=0.5)
        circle = Circle(color=YELLOW_C, fill_opacity=0.5)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
        """
        return get_filled_template(content.strip())

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = (
        "You are a Manim expert. Translate the user's math request into valid Python code "
        "inside a construct() method. Do not output markdown backticks. "
        "Use the provided variable names (BLUE_C, YELLOW_C for colors)."
    )

    full_prompt = (
        f"System: {system_prompt}\n"
        f"User: {prompt}\n"
        "Output ONLY the python code for the construct method body."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()
    
    # Remove markdown code blocks if present
    if content.startswith("```python"):
        content = content[9:-3]
    elif content.startswith("```"):
        content = content[3:-3]

    return get_filled_template(content.strip())
