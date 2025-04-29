from typing import Optional, Dict, Any
from ..models.character_classes import CharacterClass
from ..models.skills import Skill
from ..models.character import Enemy, get_fallback_enemy
from ..config.settings import STAT_RANGES
from .ai_core import generate_content
from .art_generator import generate_class_art, generate_enemy_art
import json
import random
import logging

# Define fallback classes
FALLBACK_CLASSES = [
    CharacterClass(
        name="Plague Herald",
        description="A corrupted physician who weaponizes disease and decay. Masters of pestilence who spread suffering through calculated afflictions.",
        base_health=90,
        base_attack=14,
        base_defense=4,
        base_mana=80,
        skills=[
            Skill(
                name="Virulent Outbreak",
                damage=25,
                mana_cost=20,
                description="Unleashes a devastating plague that corrupts flesh and spirit",
            ),
            Skill(
                name="Miasmic Shroud",
                damage=15,
                mana_cost=15,
                description="Surrounds self with toxic vapors that decay all they touch",
            ),
        ],
    ),
    # Add other fallback classes...
]

logger = logging.getLogger("ai")


def generate_character_class() -> Optional[CharacterClass]:
    # First provide detailed context
    context = """Create a UNIQUE dark fantasy character class.

CRITICAL JSON RULES:
1. Use ONLY the properties shown in the template
2. NO instructions or comments in property names or values
3. ALL property names must match EXACTLY as shown
4. ALL numbers must be plain integers (no decimals, no quotes)
5. ALL strings must use simple double quotes
6. NO special characters or formatting in any values
7. NO explanations or instructions in the values
8. Skills must have EXACTLY these properties: name, damage, mana_cost, description
9. NO additional or modified properties allowed
10. Description should be a simple string describing the effect"""

    # Then provide strict JSON structure with example values and valid ranges
    json_template = {
        "name": "example: Dark Harbinger",
        "description": "example: An ancient guardian corrupted by twisted hope",
        "base_health": f"pick ONE number between {STAT_RANGES['CLASS_HEALTH'][0]} and {STAT_RANGES['CLASS_HEALTH'][1]}",
        "base_attack": f"pick ONE number between {STAT_RANGES['CLASS_ATTACK'][0]} and {STAT_RANGES['CLASS_ATTACK'][1]}",
        "base_defense": f"pick ONE number between {STAT_RANGES['CLASS_DEFENSE'][0]} and {STAT_RANGES['CLASS_DEFENSE'][1]}",
        "base_mana": f"pick ONE number between {STAT_RANGES['CLASS_MANA'][0]} and {STAT_RANGES['CLASS_MANA'][1]}",
        "skills": [
            {
                "name": "example: Primary Skill",
                "damage": f"pick ONE number between {STAT_RANGES['SKILL_DAMAGE'][0]} and {STAT_RANGES['SKILL_DAMAGE'][1]}",
                "mana_cost": f"pick ONE number between {STAT_RANGES['SKILL_MANA_COST'][0]} and {STAT_RANGES['SKILL_MANA_COST'][1]}",
                "cooldown": f"pick ONE number between {STAT_RANGES['SKILL_COOLDOWN'][0]} and {STAT_RANGES['SKILL_COOLDOWN'][1]}",
                "description": "example: Primary attack description",
            },
            {
                "name": "example: Secondary Skill",
                "damage": f"pick ONE number between {STAT_RANGES['SKILL_DAMAGE'][0]} and {STAT_RANGES['SKILL_DAMAGE'][1]}",
                "mana_cost": f"pick ONE number between {STAT_RANGES['SKILL_MANA_COST'][0]} and {STAT_RANGES['SKILL_MANA_COST'][1]}",
                "cooldown": f"pick ONE number between {STAT_RANGES['SKILL_COOLDOWN'][0]} and {STAT_RANGES['SKILL_COOLDOWN'][1]}",
                "description": "example: Secondary attack description",
            },
        ],
    }

    # Combine context and JSON template in prompt
    prompt = f"{context}\n\nReturn ONLY valid JSON matching this EXACT structure (replace example values with creative content and higher stat values):\n{json.dumps(json_template, indent=2)}"

    content = generate_content(prompt)
    if not content:
        logger.error("No content generated from AI")
        return random.choice(FALLBACK_CLASSES)

    try:
        # Parse the JSON content first
        data = json.loads(content)
        logger.debug(f"Successfully parsed JSON data: {json.dumps(data, indent=2)}")

        # Create character class with processed skills
        char_data = {
            "name": str(data["name"]).strip(),
            "description": str(data["description"]).strip(),
            "base_health": int(data["base_health"]),
            "base_attack": int(data["base_attack"]),
            "base_defense": int(data["base_defense"]),
            "base_mana": int(data["base_mana"]),
            "skills": [
                Skill(
                    name=str(skill["name"]).strip(),
                    damage=int(skill["damage"]),
                    mana_cost=int(skill["mana_cost"]),
                    description=str(skill["description"]).strip(),
                )
                for skill in data["skills"]
            ],
        }

        # Create character class
        character_class = CharacterClass(**char_data)

        # Generate and attach art
        art = generate_class_art(character_class.name, character_class.description)
        if art:
            character_class.art = art.strip()

        return character_class

    except Exception as e:
        logger.error(f"Error processing character class: {str(e)}")
        logger.debug(f"Failed content was: {content}")
        return random.choice(FALLBACK_CLASSES)


def _try_parse_enemy_data(content: str) -> Optional[Dict[str, Any]]:
    """
    Try to parse enemy data from AI response.
    Returns parsed data or None if parsing failed.
    """
    try:
        # Try to parse as JSON first
        data = json.loads(content)
        return data
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract JSON-like structure
        # from the text using string manipulation
        logger.warning(
            "Failed to parse enemy data as JSON, attempting manual extraction"
        )
        try:
            # Look for opening and closing braces
            start_idx = content.find("{")
            end_idx = content.rfind("}")

            if start_idx >= 0 and end_idx > start_idx:
                # Extract potential JSON string
                json_str = content[start_idx : end_idx + 1]
                # Try to parse this extracted part
                data = json.loads(json_str)
                return data
            else:
                logger.error("Could not find valid JSON structure in the response")
                return None
        except Exception as e:
            logger.error(f"Error extracting enemy data: {str(e)}")
            return None


def generate_enemy(player_level: int) -> Enemy:
    """Generate an enemy based on player level"""
    try:
        logger.info(f"Generating enemy for player level {player_level}")

        # Generate enemy data
        prompt = f"""Create a unique enemy for a dark fantasy game where the world is corrupted by a malevolent entity known as the God of Hope.

Player level: {player_level}

Return a JSON object with:
{{
  "name": "Enemy name",
  "description": "Brief description (1-2 sentences)",
  "health": number (between {60 + player_level * 10} and {100 + player_level * 15}),
  "attack": number (between {8 + player_level * 2} and {12 + player_level * 3}),
  "defense": number (between {3 + player_level} and {6 + player_level * 2}),
  "level": number (around {player_level}, slightly higher or lower)
}}

Make the enemy thematically consistent with a world twisted by false hope.
"""

        content = generate_content(prompt)
        if not content:
            logger.error("Failed to generate enemy content, using fallback")
            return get_fallback_enemy(player_level)

        # Parse enemy data
        data = _try_parse_enemy_data(content)
        if not data:
            logger.error("Failed to parse enemy data, using fallback")
            return get_fallback_enemy(player_level)

        # Validate required fields
        required_fields = [
            "name",
            "description",
            "health",
            "attack",
            "defense",
            "level",
        ]
        for field in required_fields:
            if field not in data:
                logger.error(
                    f"Enemy data missing required field: {field}, using fallback"
                )
                return get_fallback_enemy(player_level)

        # Ensure fields are the correct types
        try:
            # Convert any string numbers to integers
            for field in ["health", "attack", "defense", "level"]:
                if isinstance(data[field], str):
                    data[field] = int(data[field])
        except (ValueError, TypeError):
            logger.error("Error converting numeric fields to integers, using fallback")
            return get_fallback_enemy(player_level)

        # Generate ASCII art for the enemy
        enemy_art = generate_enemy_art(data["name"], data["description"])

        # Calculate exp reward based on enemy level
        exp_multiplier = 15
        exp_reward = data["level"] * exp_multiplier

        # Create and return enemy
        return Enemy(
            name=data["name"],
            description=data["description"],
            health=data["health"],
            attack=data["attack"],
            defense=data["defense"],
            level=data["level"],
            exp_reward=exp_reward,
            art=enemy_art,
        )

    except Exception as e:
        logger.error(f"Error generating enemy: {str(e)}", exc_info=True)
        # Return fallback enemy in case of any error
        return get_fallback_enemy(player_level)
