from typing import Optional
from ..models.character_classes import CharacterClass
from ..models.skills import Skill
from ..models.character import Enemy
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


def generate_enemy(player_level: int = 1) -> Optional[Enemy]:
    """Generate an enemy based on player level"""
    logger.info(f"Generating enemy for player level {player_level}")

    try:
        # Generate enemy data first
        data_prompt = """Create a dark fantasy enemy corrupted by the God of Hope's invasion.

Background: The God of Hope's presence twists all it touches, corrupting beings with a perverted form of hope that drives them mad.
These creatures now roam the realm, spreading the Curse of Hope.

Guidelines:
- Should be a being corrupted by the God of Hope's influence
- Can be former holy creatures now twisted by hope
- Can be ancient beings awakened and corrupted
- Stats must be balanced for player combat
- Description should reflect their corruption by hope
- Enemy stats should scale with player level, creating stronger enemies at higher levels

STRICT JSON RULES:
- Return ONLY valid JSON matching the EXACT structure below
- Every property MUST use double quotes
- All numbers MUST be integers without decimals
- Do not add any extra properties
- No trailing commas
- No comments or explanations

Required JSON structure:
{
    "name": "string (enemy name)",
    "description": "string (enemy description)",
    "level": "integer between 1-5",
    "health": "integer between 30-100",
    "attack": "integer between 8-25",
    "defense": "integer between 2-10",
    "exp_reward": "integer between 20-100"
}"""

        content = generate_content(data_prompt)
        if not content:
            return None

        data = json.loads(content)
        logger.debug(f"Parsed enemy data: {data}")

        # Create enemy from raw stats
        enemy = Enemy(
            name=data["name"],
            description=data.get("description", ""),
            health=int(data["health"]),
            attack=int(data["attack"]),
            defense=int(data["defense"]),
            level=int(data["level"]),
            exp_reward=int(data["exp_reward"]),
            art=None,  # We'll set this later if art generation succeeds
        )

        # Generate and attach art
        try:
            art = generate_enemy_art(enemy.name, enemy.description)
            if art:
                enemy.art = art
        except Exception as art_error:
            logger.error(f"Art generation failed: {art_error}")
            # Continue without art

        logger.info(f"Successfully generated enemy: {enemy.name}")
        return enemy

    except Exception as e:
        logger.error(f"Enemy generation failed: {str(e)}")
        logger.error("Traceback: ", exc_info=True)
        return None
