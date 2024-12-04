import json
from typing import Optional, Dict, List, Tuple
from ..config.settings import AI_SETTINGS
from .ai_core import generate_content
from ..utils.pixel_art import PixelArt
from ..utils.art_utils import (
    draw_circular_shape,
    draw_tall_shape,
    add_feature,
    add_detail,
)


def generate_art_description(entity_type: str, name: str) -> Optional[Dict]:
    """Generate art description using AI"""
    prompt = f"""Create a detailed ASCII art description for a {entity_type} named '{name}' in a dark fantasy setting.
    Focus on creating a distinctive silhouette and memorable details.

    Return as JSON with these exact specifications:
    {{
        "layout": {{
            "base_shape": "main shape description",
            "key_features": ["list of 2-3 distinctive visual elements"],
            "details": ["list of 2-3 smaller details"],
            "color_scheme": {{
                "primary": [R,G,B],
                "secondary": [R,G,B],
                "accent": [R,G,B],
                "highlight": [R,G,B]
            }}
        }},
        "ascii_elements": {{
            "main_body": "character to use for main shape",
            "details": "character for details",
            "outline": "character for edges",
            "highlights": "character for glowing/accent parts"
        }}
    }}"""

    content = generate_content(prompt)
    if not content:
        return None

    try:
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing art description: {e}")
        return None


def create_pixel_art(desc: Dict, width: int = 20, height: int = 20) -> PixelArt:
    art = PixelArt(width, height)
    layout = desc["layout"]
    elements = desc["ascii_elements"]
    colors = layout["color_scheme"]

    # Convert color arrays to tuples
    color_map = {
        "primary": tuple(colors["primary"]),
        "secondary": tuple(colors["secondary"]),
        "accent": tuple(colors["accent"]),
        "highlight": tuple(colors["highlight"]),
    }

    # Draw base shape
    center_x, center_y = width // 2, height // 2
    if "circular" in layout["base_shape"].lower():
        draw_circular_shape(
            art, center_x, center_y, color_map["primary"], elements["main_body"]
        )
    elif "tall" in layout["base_shape"].lower():
        draw_tall_shape(
            art, center_x, center_y, color_map["primary"], elements["main_body"]
        )
    else:
        draw_default_shape(
            art, center_x, center_y, color_map["primary"], elements["main_body"]
        )

    # Add key features
    for feature in layout["key_features"]:
        add_feature(art, feature, color_map["secondary"], elements["details"])

    # Add highlights and details
    for detail in layout["details"]:
        add_detail(art, detail, color_map["accent"], elements["highlights"])

    return art


def generate_enemy_art(name: str) -> PixelArt:
    art = PixelArt(20, 10)

    # Color palette
    DARK_RED = (139, 0, 0)
    BLOOD_RED = (190, 0, 0)
    BONE_WHITE = (230, 230, 210)
    SHADOW = (20, 20, 20)

    if name.lower() == "skeleton":
        # Draw skeleton
        for y in range(2, 8):
            art.set_pixel(10, y, BONE_WHITE, char="█")
        # Add skull features
        art.set_pixel(9, 3, SHADOW, char="●")
        art.set_pixel(11, 3, SHADOW, char="●")
        art.set_pixel(10, 5, SHADOW, char="▀")

    elif name.lower() == "dragon":
        # Draw dragon silhouette
        for x in range(5, 15):
            for y in range(3, 7):
                art.set_pixel(x, y, BLOOD_RED, char="▄")
        # Add wings
        for x in range(3, 17):
            art.set_pixel(x, 2, DARK_RED, char="▀")

    return art


def generate_item_art(item_type: str) -> PixelArt:
    art = PixelArt(10, 10)

    # Color palette
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    LEATHER = (139, 69, 19)

    if item_type == "weapon":
        # Draw sword
        for y in range(2, 8):
            art.set_pixel(5, y, SILVER, char="│")
        art.set_pixel(5, 2, GOLD, char="◆")

    elif item_type == "armor":
        # Draw armor
        for x in range(3, 7):
            for y in range(3, 7):
                art.set_pixel(x, y, LEATHER, char="▒")

    return art


def generate_class_art(class_name: str) -> PixelArt:
    art = PixelArt(20, 20)

    # Enhanced color palette
    DARK = (30, 30, 40)
    MAIN = (80, 80, 100)
    ACCENT = (140, 20, 20)
    HIGHLIGHT = (200, 200, 220)
    GLOW = (180, 180, 220)

    # Draw base character silhouette
    for y in range(4, 16):
        for x in range(7, 14):
            art.set_pixel(x, y, MAIN, char="█")

    # Class-specific details
    name_lower = class_name.lower()
    if "hope" in name_lower or "bane" in name_lower:
        # Corrupted holy warrior
        for y in range(4, 16):
            art.set_pixel(6, y, DARK, char="░")
            art.set_pixel(14, y, DARK, char="░")
        # Corrupted halo
        for x in range(7, 14):
            art.set_pixel(x, 3, ACCENT, char="▄")
        # Glowing eyes
        art.set_pixel(8, 6, GLOW, char="●")
        art.set_pixel(12, 6, GLOW, char="●")

    elif "herald" in name_lower:
        # Plague Herald with miasma
        for y in range(3, 17):
            art.set_pixel(5, y, DARK, char="░")
            art.set_pixel(15, y, DARK, char="░")
        # Hood
        for x in range(7, 14):
            art.set_pixel(x, 4, DARK, char="▀")
        # Mask
        art.set_pixel(9, 6, ACCENT, char="◣")
        art.set_pixel(11, 6, ACCENT, char="◢")

    elif "sovereign" in name_lower:
        # Blood Sovereign with crown and regal details
        for x in range(6, 15):
            art.set_pixel(x, 3, ACCENT, char="♦")
        # Cape
        for y in range(5, 15):
            art.set_pixel(5, y, MAIN, char="║")
            art.set_pixel(15, y, MAIN, char="║")
        # Glowing eyes
        art.set_pixel(8, 6, GLOW, char="◆")
        art.set_pixel(12, 6, GLOW, char="◆")

    return art
