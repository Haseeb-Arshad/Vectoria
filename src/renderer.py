import subprocess
import sys
import os

def render_scene(code: str, file_name: str) -> str:
    """
    Renders the given Manim code using the Manim CLI.
    Returns the path to the generated .mp4 file.
    """
    # Create temp directory if it doesn't exist
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    temp_file_path = os.path.join(temp_dir, f"{file_name}.py")
    
    with open(temp_file_path, "w") as f:
        f.write(code)
    
    # Ensure output directory exists
    output_dir = os.path.abspath("output")
    os.makedirs(output_dir, exist_ok=True)

    # Manim command: manim -qm --media_dir ./output temp_file.py GenScene
    cmd = [
        "manim",
        "-qm",  # Medium quality by default
        "--media_dir", output_dir,
        temp_file_path,
        "GenScene"
    ]

    try:
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            check=True
        )
    except subprocess.CalledProcessError as e:
        error_message = f"Manim failed with return code {e.returncode}.\nStderr: {e.stderr}"
        raise RuntimeError(error_message) from e
    
    # Construct expected output path
    # Manim default structure: media_dir/videos/scene_name/quality/SceneName.mp4
    # With -qm, it's usually videos/scenes/720p30/GenScene.mp4 if relying on defaults,
    # but with --media_dir it might change.
    # Actually, manim outputs to <media_dir>/videos/<module_name>/<quality>/<scene_name>.mp4
    # Here module name is `file_name` (from temp_file_path).
    
    # Let's try to find the file or predictable path
    # output/videos/file_name/720p30/GenScene.mp4
    video_path = os.path.join(output_dir, "videos", file_name, "720p30", "GenScene.mp4")
    
    if not os.path.exists(video_path):
         # Fallback search if path prediction fails
         for root, dirs, files in os.walk(output_dir):
             for file in files:
                 if file.endswith("GenScene.mp4"):
                     return os.path.join(root, file)
         raise FileNotFoundError(f"Could not locate output video at {video_path}")

    return video_path
