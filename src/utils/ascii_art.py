import os
from ..services.art_generator import generate_class_art
from ..utils.pixel_art import PixelArt
from typing import Optional
from src.config.settings import ENABLE_AI_CLASS_GENERATION


def convert_pixel_art_to_ascii(pixel_art):
    """Convert pixel art to ASCII art."""
    ascii_art = ""
    for row in pixel_art:
        for pixel in row:
            if pixel == 0:
                ascii_art += " "
            else:
                ascii_art += "#"
        ascii_art += "\n"
    return ascii_art


def display_ascii_art(art):
    """Display ASCII art or PixelArt in the terminal."""
    if isinstance(art, PixelArt):
        print(art.render())
    elif isinstance(art, str):
        print(art)
    else:
        print("Unsupported art format")


def save_ascii_art(art: PixelArt, filename: str):
    """Save ASCII art to file"""
    os.makedirs("data/art", exist_ok=True)
    safe_filename = filename.lower().replace("'", "").replace(" ", "_")
    filepath = f"data/art/{safe_filename}.txt"

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(art.render())
    except Exception as e:
        print(f"Error saving art: {e}")


def load_ascii_art(filename: str) -> Optional[str]:
    """Load ASCII art from file"""
    safe_filename = filename.lower().replace("'", "").replace(" ", "_")
    filepath = f"data/art/{safe_filename}.txt"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading art: {e}")
        return None


def ensure_character_art(class_name: str) -> str:
    """Generate and save character art if it doesn't exist"""
    safe_name = class_name.lower().replace("'", "").replace(" ", "_") + ".txt"
    art_path = os.path.join("data/art", safe_name)

    if not os.path.exists(art_path):
        if ENABLE_AI_CLASS_GENERATION:
            art = generate_class_art(class_name)
            save_ascii_art(art, safe_name)
        else:
            return ""  # Return empty string if AI generation is disabled

    return safe_name
