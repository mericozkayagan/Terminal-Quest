import os
from typing import Optional, Union
from src.config.settings import ENABLE_AI_ART_GENERATION
from src.services.art_generator import (
    generate_class_art,
    generate_enemy_art,
    generate_item_art,
)
from src.utils.pixel_art import PixelArt


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


def save_ascii_art(art: Union[PixelArt, str], filename: str):
    """Save ASCII art to file"""
    os.makedirs("data/art", exist_ok=True)
    safe_filename = filename.lower().replace("'", "").replace(" ", "_")
    filepath = f"data/art/{safe_filename}.txt"

    try:
        content = art.render() if isinstance(art, PixelArt) else str(art)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
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


def ensure_entity_art(entity_name: str, entity_type: str, description: str = "") -> str:
    """Generate and save art for any entity if it doesn't exist"""
    safe_name = (
        f"{entity_type}_{entity_name.lower().replace(' ', '_').replace("'", '')}"
    )
    art_path = os.path.join("data/art", f"{safe_name}.txt")

    if not os.path.exists(art_path):
        if ENABLE_AI_ART_GENERATION:
            art_func = {
                "class": generate_class_art,
                "enemy": generate_enemy_art,
                "item": generate_item_art,
            }.get(entity_type)

            if art_func:
                art = art_func(entity_name, description)
                if art:
                    save_ascii_art(art, safe_name)
                else:
                    return ""
        else:
            return ""

    return safe_name
