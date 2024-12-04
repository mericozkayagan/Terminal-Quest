from typing import Optional
from ..models.character_classes import CharacterClass
from ..models.skills import Skill
from ..models.character import Enemy
from ..config.settings import STAT_RANGES
from .ai_core import generate_content
from .art_generator import generate_art_description, create_pixel_art
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
                "description": "example: Primary attack description",
            },
            {
                "name": "example: Secondary Skill",
                "damage": f"pick ONE number between {STAT_RANGES['SKILL_DAMAGE'][0]} and {STAT_RANGES['SKILL_DAMAGE'][1]}",
                "mana_cost": f"pick ONE number between {STAT_RANGES['SKILL_MANA_COST'][0]} and {STAT_RANGES['SKILL_MANA_COST'][1]}",
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

        # Create and validate the character class
        character_class = CharacterClass(**char_data)
        logger.debug(f"Successfully created character class: {character_class.name}")
        return character_class

    except Exception as e:
        logger.error(f"Error processing character class: {str(e)}")
        logger.debug(f"Failed content was: {content}")
        return random.choice(FALLBACK_CLASSES)


def generate_enemy() -> Optional[Enemy]:
    prompt = """Create a dark fantasy enemy corrupted by the God of Hope's invasion.

Background: The God of Hope's presence twists all it touches, corrupting beings with a perverted form of hope that drives them mad.
These creatures now roam the realm, spreading the Curse of Hope.

Guidelines:
- Should be a being corrupted by the God of Hope's influence
- Can be former holy creatures now twisted by hope
- Can be ancient beings awakened and corrupted
- Stats must be balanced for player combat
- Description should reflect their corruption by hope

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
    "description": "string (2-3 sentences about corruption)",
    "health": f"integer between {STAT_RANGES['ENEMY_HEALTH'][0]}-{STAT_RANGES['ENEMY_HEALTH'][1]}",
    "attack": f"integer between {STAT_RANGES['ENEMY_ATTACK'][0]}-{STAT_RANGES['ENEMY_ATTACK'][1]}",
    "defense": f"integer between {STAT_RANGES['ENEMY_DEFENSE'][0]}-{STAT_RANGES['ENEMY_DEFENSE'][1]}",
    "exp": f"integer between {STAT_RANGES['ENEMY_EXP'][0]}-{STAT_RANGES['ENEMY_EXP'][1]}",
    "gold": f"integer between {STAT_RANGES['ENEMY_GOLD'][0]}-{STAT_RANGES['ENEMY_GOLD'][1]}"
}"""

    content = generate_content(prompt)
    if not content:
        return None

    try:
        data = json.loads(content)
        # Validate and normalize stats
        stats = {
            "health": (30, 100),
            "attack": (8, 25),
            "defense": (2, 10),
            "exp": (20, 100),
            "gold": (10, 100),
        }

        for stat, (min_val, max_val) in stats.items():
            data[stat] = max(min_val, min(max_val, int(data[stat])))

        art_desc = generate_art_description("enemy", data["name"])
        if art_desc:
            enemy = Enemy(**data)
            enemy.art = create_pixel_art(art_desc)
            return enemy

        return Enemy(**data)
    except Exception as e:
        print(f"\nError processing enemy: {e}")
        return None
