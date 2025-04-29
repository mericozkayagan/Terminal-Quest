from typing import Optional, Dict, Any
from dataclasses import dataclass
import logging
from src.utils.json_cleaner import JSONCleaner
from .ai_core import generate_content
import random

logger = logging.getLogger(__name__)


@dataclass
class ArtGenerationConfig:
    width: int = 30
    height: int = 15
    max_retries: int = 3
    style: str = "dark fantasy"
    border: bool = True
    characters: str = "░▒▓█▀▄╱╲╳┌┐└┘│─├┤┬┴┼╭╮╯╰◣◢◤◥╱╲╳▁▂▃▅▆▇◆♦⚊⚋╍╌┄┅┈┉"


LORE = {
    "world": """In an age where hope became poison, darkness emerged as salvation.
    The God of Hope's invasion brought not comfort, but corruption - a twisted force
    that warps reality with false promises and maddening light. Those touched by
    this 'Curse of Hope' become enslaved to eternal, desperate optimism, their minds
    fractured by visions of impossible futures. The curse manifests physically,
    marking its victims with radiant cracks in their flesh that leak golden light.

    Only those who embrace shadow, who shield their eyes from hope's blinding rays,
    maintain their sanity. They are the last bastion against the spreading taint,
    warriors who understand that in this fallen realm, true salvation lies in the
    comforting embrace of darkness.""",
    "class": """Champions who've learned to weaponize shadow itself, these warriors
    bear dark sigils that protect them from hope's corruption. Each class represents
    a different approach to surviving in a world where optimism kills and despair
    shields. Their powers draw from the void between false hopes, turning the
    absence of light into a force of preservation.""",
    "enemy": """Victims of the Curse of Hope, these beings are twisted parodies of
    their former selves. Holy knights whose zealous hope turned to madness, common
    folk whose desperate wishes mutated them, and ancient guardians whose protective
    nature was perverted by the God of Hope's touch. They radiate a sickly golden
    light from their wounds, and their mouths eternally smile even as they destroy
    all they once loved.""",
    "item": """Artifacts of power in this darkened realm take two forms: those
    corrupted by the God of Hope's touch, glowing with insidious golden light and
    whispering false promises; and those forged in pure darkness, their surfaces
    drinking in light itself. The corrupted items offer tremendous power at the cost
    of slowly succumbing to hope's curse, while shadow-forged gear helps resist the
    spreading taint.""",
}


def _generate_art(
    prompt: str, config: ArtGenerationConfig = ArtGenerationConfig()
) -> Optional[str]:
    """Internal function to handle art generation with retries and validation.

    Args:
        prompt: The generation prompt
        config: Art generation configuration settings

    Returns:
        Optional[str]: The generated and cleaned ASCII art, or None if generation fails
    """
    for attempt in range(config.max_retries):
        try:
            content = generate_content(prompt)
            if not content:
                continue

            cleaned_art = JSONCleaner.clean_art_content(content)
            if not cleaned_art:
                continue

            # Validate dimensions and characters
            lines = cleaned_art.split("\n")
            if len(lines) > config.height:
                lines = lines[: config.height]

            valid_chars = set(config.characters)
            filtered_lines = []
            for line in lines:
                # Trim line to max width
                line = line[: config.width]
                # Filter out invalid characters
                filtered_line = "".join(
                    c if c in valid_chars or c in "║╔╗╚╝ " else " " for c in line
                )
                # Pad line to exact width
                filtered_line = filtered_line.ljust(config.width)
                filtered_lines.append(filtered_line)

            # Pad to exact height
            while len(filtered_lines) < config.height:
                filtered_lines.append(" " * config.width)

            return "\n".join(filtered_lines)

        except Exception as e:
            logger.error(f"Art generation attempt {attempt + 1} failed: {e}")
            continue

    logger.error("All art generation attempts failed")
    return None


def generate_enemy_art(enemy_name: str, enemy_description: str) -> str:
    """Generate detailed ASCII art for corrupted enemies"""
    prompt = f"""Create a corrupted being ASCII art for '{enemy_name}'.

World Lore: {LORE['world']}
Enemy Lore: {LORE['enemy']}
Creature Description: {enemy_description}

Requirements:
1. Use ONLY these characters: {ArtGenerationConfig.characters}
2. Create EXACTLY 8 lines of art
3. Each line must be EXACTLY 30 characters
4. Focus on CORRUPTION features:
   - Twisted holy symbols
   - False hope's radiance
   - Corrupted flesh/form
   - Madness in their features
   - Signs of former nobility/purity

Example format:
╔═══════════════════════════╗
║     ▄▄████████████▄▄      ║
║   ▄█▓░╱║██████║╲░▓█▄      ║
║  ██▓█▀▀╚════╝▀▀█▓██       ║
║  ███╔═▓░▄▄▄▄░▓═╗███       ║
║  ▀██║░▒▓████▓▒░║██▀       ║
║   ██╚═▓▓▓██▓▓▓═╝██        ║
║    ▀▀████▀▀████▀▀         ║
╚═══════════════════════════╝

Return ONLY the raw ASCII art."""

    try:
        # Use the _generate_art function to ensure proper formatting and validation
        content = _generate_art(prompt, ArtGenerationConfig(width=30, height=8))
        if content:
            return content

        return get_default_enemy_art()
    except Exception as e:
        logger.error(f"Error in enemy art generation: {str(e)}")
        return get_default_enemy_art()


def generate_item_art(item_name: str, description: str) -> Optional[str]:
    """Generate detailed ASCII art for dark artifacts"""
    prompt = f"""Create a dark artifact ASCII art for '{item_name}'.

World Lore: {LORE['world']}
Item Lore: {LORE['item']}
Artifact Description: {description}

Requirements:
1. Use ONLY these characters: {ArtGenerationConfig.characters}
2. Create EXACTLY 6 lines of art
3. Each line must be EXACTLY 20 characters
4. Focus on ARTIFACT features:
   - Anti-hope wards
   - Shadow essence flows
   - Corrupted or pure state
   - Power runes/symbols
   - Material composition

Example format:
╔═══════════════════════════╗
║  ▄▄████████▄   ║
║ █▓░◆═══◆░▓█   ║
║ ██╲▓▓██▓▓╱██  ║
║  ▀█▄░──░▄█▀   ║
╚════════════════╝

Return ONLY the raw ASCII art."""

    return _generate_art(prompt)


def generate_class_art(class_name: str, description: str = "") -> str:
    """Generate detailed ASCII art for character classes"""
    prompt = f"""Create a dark fantasy character portrait ASCII art for '{class_name}'.

World Lore: {LORE['world']}
Class Lore: {LORE['class']}
Character Description: {description}

Requirements:
1. Use ONLY these characters: {ArtGenerationConfig.characters}
2. Create EXACTLY 15 lines of art
3. Each line must be EXACTLY 30 characters
4. Focus on DARK CHAMPION features:
   - Stern, determined facial expression
   - Dark armor with shadow essence
   - Anti-hope runes and wards
   - Class-specific weapons/items
   - Signs of resistance against hope

Example format:
╔════════════════════════════════╗
║      ▄▄███████████▄▄           ║
║    ▄█▀▀░░░░░░░░░▀▀█▄           ║
║   ██░▒▓████████▓▒░██           ║
║  ██░▓█▀╔══╗╔══╗▀█▓░██          ║
║  █▓▒█╔══║██║══╗█▒▓█            ║
║  █▓▒█║◆═╚══╝═◆║█▒▓█            ║
║  ██▓█╚════════╝█▓██            ║
║   ███▀▀══════▀▀███             ║
║  ██╱▓▓▓██████▓▓▓╲██            ║
║ ██▌║▓▓▓▓▀██▀▓▓▓▓║▐██           ║
║ ██▌║▓▓▓▓░██░▓▓▓▓║▐██           ║
║  ██╲▓▓▓▓░██░▓▓▓▓╱██            ║
║   ███▄▄░████░▄▄███             ║
╚════════════════════════════════╝

Return ONLY the raw ASCII art."""

    try:
        # Use the _generate_art function for consistent formatting
        content = _generate_art(prompt, ArtGenerationConfig(width=30, height=15))
        if content:
            return content

        return get_default_class_art()
    except Exception as e:
        logger.error(f"Error in class art generation: {str(e)}")
        return get_default_class_art()


def generate_ascii_portrait(character_name: str, character_description: str) -> str:
    """Generate detailed ASCII art portrait for an NPC or character"""
    prompt = f"""Create a detailed ASCII art portrait for a dark fantasy character named '{character_name}'.

Character Description: {character_description}
World Lore: {LORE['world']}

Requirements:
1. Use ONLY these characters: {ArtGenerationConfig.characters}
2. Create EXACTLY 13 lines of art
3. Each line must be EXACTLY 35 characters
4. Focus on CHARACTER features:
   - Distinctive facial features
   - Clothing and accessories
   - Signs of corruption or resistance to hope
   - Expressions that reflect their nature
   - Full upper body if possible

Example format:
╔═══════════════════════════════════╗
║         ▄▄████████▄▄              ║
║       ▄█▓░╱║██████║╲░▓█▄          ║
║      ██▓█▀▀╚════╝▀▀█▓██           ║
║      ███╔═▓░▄▄▄▄░▓═╗███           ║
║      ▀██║░▒▓████▓▒░║██▀           ║
║       ██╚═▓▓▓██▓▓▓═╝██            ║
║        ▀▀████▀▀████▀▀             ║
║         ██▀▀░██░▀▀██              ║
║        ▄█▌░▒▄██▄▒░▐█▄             ║
║       ▄█░▒▓█▀██▀█▓▒░█▄            ║
║      ██▀▄▄▄▄▄██▄▄▄▄▄▀██           ║
╚═══════════════════════════════════╝

Return ONLY the raw ASCII art."""

    try:
        content = _generate_art(prompt, ArtGenerationConfig(width=35, height=13))
        if content:
            return content

        return get_default_npc_art(character_name)
    except Exception as e:
        logger.error(f"Error in portrait art generation: {str(e)}")
        return get_default_npc_art(character_name)


def get_default_enemy_art() -> str:
    """Return a default ASCII art for enemies when generation fails"""
    default_arts = [
        """
╔═══════════════════════════╗
║     ▄▄████████████▄▄      ║
║   ▄█▓░╱║██████║╲░▓█▄      ║
║  ██▓█▀▀╚════╝▀▀█▓██       ║
║  ███╔═▓░▄▄▄▄░▓═╗███       ║
║  ▀██║░▒▓████▓▒░║██▀       ║
║   ██╚═▓▓▓██▓▓▓═╝██        ║
║    ▀▀████▀▀████▀▀         ║
╚═══════════════════════════╝
""",
        """
╔═══════════════════════════╗
║      ▄▄██████████▄▄       ║
║    ▄█▓░░░╳░░░░╳░░▓█▄      ║
║   ██▓█▀▀◣◢◤◥▀▀█▓██        ║
║   ███╔══▒▓██▓▒══╗███      ║
║   ▀██╝◆═══════◆╚██▀       ║
║    ██▄▄████████▄▄██       ║
║     █░▄▀▀▀██▀▀▀▄░█        ║
╚═══════════════════════════╝
""",
        """
╔═══════════════════════════╗
║     ▄▄▄███████▄▄▄         ║
║    █▓░▄▀▓██████▓▀▄░▓█     ║
║   ██▓█▀░▒▓▒░░▒▓▒░▀█▓██    ║
║  ██▓╔═┼─◆─◆─┼═╗▓██        ║
║  ██▓║▒▒▒████▒▒▒║▓██       ║
║   ██┴─▀▀◆══◆▀▀─┴██        ║
║    █▄░▒▒▒▓░░▓▒▒▒░▄█        ║
╚═══════════════════════════╝
""",
    ]
    return random.choice(default_arts)


def get_default_class_art() -> str:
    """Return a default ASCII art for character classes when generation fails"""
    default_arts = [
        """
╔════════════════════════════════╗
║      ▄▄███████████▄▄           ║
║    ▄█▀▀░░░░░░░░░▀▀█▄           ║
║   ██░▒▓████████▓▒░██           ║
║  ██░▓█▀╔══╗╔══╗▀█▓░██          ║
║  █▓▒█╔══║██║══╗█▒▓█            ║
║  █▓▒█║◆═╚══╝═◆║█▒▓█            ║
║  ██▓█╚════════╝█▓██            ║
║   ███▀▀══════▀▀███             ║
║  ██╱▓▓▓██████▓▓▓╲██            ║
║ ██▌║▓▓▓▓▀██▀▓▓▓▓║▐██           ║
║ ██▌║▓▓▓▓░██░▓▓▓▓║▐██           ║
║  ██╲▓▓▓▓░██░▓▓▓▓╱██            ║
║   ███▄▄░████░▄▄███             ║
╚════════════════════════════════╝
""",
        """
╔════════════════════════════════╗
║       ▄▄██████████▄▄           ║
║     ▄█▀░░▓██████▓░░▀█▄         ║
║    ██▓░▒┼═┼══┼═┼▒░▓██          ║
║   ██▓╔══╗▓██████▓╔══╗▓██       ║
║   ██▓║◆◆║██████║◆◆║▓██         ║
║   ██▓╚══╝▓██████▓╚══╝▓██       ║
║    ███░░╱╲██████╱╲░░███        ║
║    ▄█▀▓▓▓██████████▓▓▓▀█▄      ║
║   ▄█▓░▒████████████▒░▓█▄       ║
║  ██▓░▓▓█▀██████▀█▓▓░▓██        ║
║  ██▓╔═╝█▓██████▓█╚═╗▓██        ║
║  ███╚══▓██████████══╝███       ║
║   ███▄▄██████████▄▄███         ║
╚════════════════════════════════╝
""",
        """
╔════════════════════════════════╗
║       ▄▄█████████▄▄            ║
║     ▄█▀░░░▓████▓░░░▀█▄         ║
║    ██▓░▒▒▒██████▒▒▒░▓██        ║
║   ██▓░▓▀╔══╗╔══╗▀▓░▓██         ║
║   ██▓║╲░║██████║░╱║▓██         ║
║   ██▓╝◆═╚══╝╚══╝═◆╚▓██         ║
║    ███▓▒▒██████▒▒▓███          ║
║     ██▒▓▓██████▓▓▒██           ║
║    ██╱╱╲╲██████╱╱╲╲██          ║
║   ██▌░░░░██████░░░░▐██         ║
║   ██▌╔══╗██████╔══╗▐██         ║
║    ██╚═▓▓██████▓▓═╝██          ║
║     ███▄▄██████▄▄███           ║
╚════════════════════════════════╝
""",
    ]
    return random.choice(default_arts)


def get_default_npc_art(npc_name: str = "") -> str:
    """Return a detailed default ASCII art for NPCs when generation fails"""
    default_arts = [
        """
╔═══════════════════════════════════╗
║         ▄▄████████▄▄              ║
║       ▄█▓░╱║██████║╲░▓█▄          ║
║      ██▓█▀▀╚════╝▀▀█▓██           ║
║      ███╔═▓░▄▄▄▄░▓═╗███           ║
║      ▀██║░▒▓████▓▒░║██▀           ║
║       ██╚═▓▓▓██▓▓▓═╝██            ║
║        ▀▀████▀▀████▀▀             ║
║         ██▀▀░██░▀▀██              ║
║        ▄█▌░▒▄██▄▒░▐█▄             ║
║       ▄█░▒▓█▀██▀█▓▒░█▄            ║
║      ██▀▄▄▄▄▄██▄▄▄▄▄▀██           ║
╚═══════════════════════════════════╝
""",
        """
╔═══════════════════════════════════╗
║           ▄▄███▄▄                 ║
║        ▄██▓▒░░░▒▓██▄              ║
║       ██▓░▒▓██▓▒░▓██              ║
║      ██░▓█╔═╗╔═╗█▓░██             ║
║      █▓▒█║▒╚╝▒╚╝║█▒▓█             ║
║      █▓▒█╚════════╝█▒▓█           ║
║      ██▓█░▒▒▒▓▓▒▒▒░█▓██           ║
║       ███░▒▓████▓▒░███            ║
║      ██╱▓▓▓▓████▓▓▓▓╲██           ║
║     ██▌║▓▓▓▓░██░▓▓▓▓║▐██          ║
║     ██▌║▓▓▓▓░██░▓▓▓▓║▐██          ║
╚═══════════════════════════════════╝
""",
        """
╔═══════════════════════════════════╗
║           ▄▄█████▄▄               ║
║        ▄█▀▀░░░░░░░▀▀█▄            ║
║       ██░▒▓████████▓▒░██          ║
║      ██░▓█▀╔══╗╔══╗▀█▓░██         ║
║      █▓▒█╔══║██║══╗█▒▓█           ║
║      █▓▒█║◆═╚══╝═◆║█▒▓█           ║
║      ██▓█╚════════╝█▓██           ║
║       ███▀▀══════▀▀███            ║
║      ██╱▓▓▓██████▓▓▓╲██           ║
║     ██▌║▓▓▓▓▀██▀▓▓▓▓║▐██          ║
║     ██▌║▓▓▓▓░██░▓▓▓▓║▐██          ║
╚═══════════════════════════════════╝
""",
    ]
    return random.choice(default_arts)
