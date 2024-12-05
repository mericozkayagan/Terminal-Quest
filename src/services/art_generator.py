import json
from typing import Optional, Dict, List, Tuple
from ..config.settings import AI_SETTINGS
from .ai_core import generate_content
from ..utils.pixel_art import PixelArt
from ..utils.art_utils import (
    draw_circular_shape,
    draw_default_shape,
    draw_tall_shape,
    add_feature,
    add_detail,
    load_ascii_art,
)
import logging
import time

logger = logging.getLogger(__name__)


def generate_ascii_art(
    entity_type: str, name: str, width: int = 20, height: int = 10
) -> Optional[str]:
    """Generate ASCII art using text prompts"""
    prompt = f"""Create a {width}x{height} ASCII art for a {entity_type} named '{name}' in a dark fantasy setting.
    Rules:
    1. Use ONLY these characters: ░ ▒ ▓ █ ▄ ▀ ║ ═ ╔ ╗ ╚ ╝ ♦ ◆ ◢ ◣
    2. Output EXACTLY {height} lines
    3. Each line must be EXACTLY {width} characters wide
    4. NO explanations or comments, ONLY the ASCII art
    5. Create a distinctive silhouette that represents the character
    6. Use darker characters (▓ █) for main body
    7. Use lighter characters (░ ▒) for details
    8. Use special characters (♦ ◆) for highlights

    Example format:
    ╔════════════╗
    ║  ▄▀▄▀▄▀▄   ║
    ║   ▓█▓█▓    ║
    ║    ◆◆◆     ║
    ╚════════════╝
    """

    content = generate_content(prompt)
    return content if content else None


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
    else:
        raise ValueError(f"Unknown enemy name: {name}")

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


def get_art_path(art_name):
    # Remove any file extension if present
    art_name = art_name.split(".")[0]
    # Return the correct path format
    return f"{art_name}.txt"


def load_monster_art(monster_name):
    art_path = get_art_path(monster_name)
    return load_ascii_art(art_path)


def generate_class_ascii_art(
    class_name: str, description: str, max_retries: int = 3
) -> Optional[str]:
    """Generate ASCII art for a character class with retries"""
    logger = logging.getLogger(__name__)

    for attempt in range(max_retries):
        try:
            prompt = f"""Create a 15x30 detailed human portrait ASCII art for the dark fantasy class '{class_name}'.
            Class description: {description}

            Rules:
            1. Use these characters for facial features and details:
               ░ ▒ ▓ █ ▀ ▄ ╱ ╲ ╳ ┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ╭ ╮ ╯ ╰
               ◣ ◢ ◤ ◥ ╱ ╲ ╳ ▁ ▂ ▃ ▅ ▆ ▇ ◆ ♦ ⚊ ⚋ ╍ ╌ ┄ ┅ ┈ ┉
            2. Create EXACTLY 15 lines of art
            3. Each line must be EXACTLY 30 characters
            4. Return ONLY the raw ASCII art, no JSON, no quotes
            5. Focus on DETAILED HUMAN FACE and upper body where:
               - Use shading (░▒▓█) for skin tones and shadows
               - Show detailed facial features (eyes, nose, mouth)
               - Include hair with flowing details
               - Add class-specific headgear/hood/crown
               - Show shoulders and upper chest with armor/clothing

            Example format for a Dark Knight:
            ╔════════════════════════════════╗
            ║      ▄▄███████████▄▄          ║
            ║    ▄█▀▀░░░░░░░░░▀▀█▄         ║
            ║   ██░▒▓████████▓▒░██         ║
            ║  ██░▓█▀╔══╗╔══╗▀█▓░██        ║
            ║  █▓▒█╔══║██║══╗█▒▓█         ║
            ║  █▓▒█║◆═╚══╝═◆║█▒▓█         ║
            ║  ██▓█╚════════╝█▓██         ║
            ║   ███▀▀══════▀▀███          ║
            ║  ██╱▓▓▓██████▓▓▓╲██         ║
            ║ ██▌║▓▓▓▓▀██▀▓▓▓▓║▐██        ║
            ║ ██▌║▓▓▓▓░██░▓▓▓▓║▐██        ║
            ║  ██╲▓▓▓▓░██░▓▓▓▓╱██         ║
            ║   ███▄▄░████░▄▄███          ║
            ╚════════════════════════════════╝

            Create similarly styled PORTRAIT art for {class_name} that shows:
            {description}

            Key elements to include:
            1. Detailed facial structure with shading
            2. Expressive eyes showing character's nature
            3. Class-specific headwear or markings
            4. Distinctive hair or hood design
            5. Shoulder armor or clothing details
            6. Magical effects or corruption signs
            7. Background shading for depth
            """

            content = generate_content(prompt)
            if not content:
                logger.warning(f"Attempt {attempt + 1}: No content generated")
                continue

            # Clean up and validation code remains the same...
            if content.strip().startswith("{"):
                try:
                    data = json.loads(content)
                    if "art" in data or "ascii_art" in data or "character_art" in data:
                        art_lines = (
                            data.get("art")
                            or data.get("ascii_art")
                            or data.get("character_art")
                        )
                        return "\n".join(art_lines)
                except json.JSONDecodeError:
                    cleaned_content = (
                        content.replace("{", "").replace("}", "").replace('"', "")
                    )
                    if "║" in cleaned_content or "╔" in cleaned_content:
                        return cleaned_content.strip()
            else:
                if "║" in content or "╔" in content:
                    return content.strip()

            logger.warning(f"Attempt {attempt + 1}: Invalid art format received")

        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")

        if attempt < max_retries - 1:
            time.sleep(1)

    return generate_fallback_art(class_name)


def generate_fallback_art(class_name: str) -> str:
    """Generate a detailed portrait fallback ASCII art"""
    return f"""╔════════════════════════════════╗
║      ▄▄███████████▄▄          ║
║    ▄█▀▀░░░░░░░░░▀▀█▄         ║
║   ██░▒▓████████▓▒░██         ║
║  ██░▓█▀╔══╗╔══╗▀█▓░██        ║
║  █▓▒█╔══║██║══╗█▒▓█         ║
║  █▓▒█║◆═╚══╝═◆║█▒▓█         ║
║  ██▓█╚════════╝█▓██         ║
║   ███▀▀══════▀▀███          ║
║  ██╱▓▓▓██████▓▓▓╲██         ║
║ ██▌║▓▓▓▓▀██▀▓▓▓▓║▐██        ║
║ ██▌║▓▓▓▓░██░▓▓▓▓║▐██        ║
║  ██╲▓▓▓▓░██░▓▓▓▓╱██         ║
║   ███▄▄░████░▄▄███          ║
╚════════════════════════════════╝"""
