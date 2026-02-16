import typer
import shutil
import os
import subprocess
from typing import Optional
from dotenv import load_dotenv
from src import generator, renderer
from rich.console import Console
from rich.prompt import Confirm

load_dotenv()
app = typer.Typer(name="animath", help="CLI for generating math animations.")
console = Console()

@app.command()
def create(
    prompt: str = typer.Argument(..., help="Description of the animation"),
    mock: bool = typer.Option(False, "--mock", help="Use mock mode (no API call).")
):
    """
    Generate and render a math animation from a prompt.
    """
    
    # 1. Generate Code
    with console.status("[bold green]Dreaming in Math...", spinner="dots"):
        try:
            code = generator.generate_manim_code(prompt, mock=mock)
        except Exception as e:
            console.print(f"[bold red]Generation failed:[/bold red] {e}")
            raise typer.Exit(code=1)

    # 2. Render Video
    with console.status("[bold blue]Rendering pixels...", spinner="dots"):
        try:
            # simple file name from prompt or timestamp could be better, but 'scene' is fine for temp
            video_path = renderer.render_scene(code, "generated_scene")
        except Exception as e:
            console.print(f"[bold red]Rendering failed:[/bold red] {e}")
            raise typer.Exit(code=1)

    console.print(f"[bold green]Success![/bold green] Video saved at: [underline]{video_path}[/underline]")
    
    if Confirm.ask("Open video now?"):
        if os.name == 'nt':  # Windows
            os.startfile(video_path)
        elif os.name == 'posix':  # macOS/Linux
            opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
            subprocess.call([opener, video_path])

@app.command(name="check-env")
def check_env():
    """
    Check if required tools (ffmpeg, latex) are installed.
    """
    ffmpeg = shutil.which("ffmpeg")
    latex = shutil.which("latex")  # or pdflatex

    if ffmpeg:
        console.print(f"[green]✔ ffmpeg found:[/green] {ffmpeg}")
    else:
        console.print("[red]✘ ffmpeg not found.[/red] Please install ffmpeg.")

    if latex:
        console.print(f"[green]✔ latex found:[/green] {latex}")
    else:
        console.print("[red]✘ latex not found.[/red] Please install a LaTeX distribution (e.g., TeX Live, MiKTeX).")

if __name__ == "__main__":
    app()
