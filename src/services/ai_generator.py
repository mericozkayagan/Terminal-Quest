from openai import OpenAI
import json
import time
import os
from typing import Optional
from ..models.character_classes import CharacterClass
from ..models.skills import Skill
from ..models.character import Enemy
from ..config.settings import AI_SETTINGS, STAT_RANGES


def setup_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No OpenAI API key found in environment variables")
    return OpenAI(api_key=api_key)


def generate_content(prompt: str, retries: int = None) -> Optional[str]:
    if retries is None:
        retries = AI_SETTINGS["MAX_RETRIES"]

    client = setup_openai()

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a dark fantasy RPG content generator focused on creating balanced game elements. Respond only with valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=AI_SETTINGS["TEMPERATURE"],
                max_tokens=AI_SETTINGS["MAX_TOKENS"],
                presence_penalty=AI_SETTINGS["PRESENCE_PENALTY"],
                frequency_penalty=AI_SETTINGS["FREQUENCY_PENALTY"],
            )
            content = response.choices[0].message.content.strip()
            json.loads(content)  # Validate JSON
            return content
        except Exception as e:
            print(f"\nAttempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                return None
            time.sleep(1)


def generate_character_class() -> Optional[CharacterClass]:
    prompt = f"""Create a unique dark fantasy character class following these guidelines:
- Must be morally ambiguous or corrupted
- Powers should involve darkness, corruption, or forbidden magic
- Stats must be balanced for gameplay
- Skills should have clear combat applications

Return as JSON:
{{
    "name": "unique class name",
    "description": "2-3 sentences about the class's dark nature and powers",
    "base_health": "number between {STAT_RANGES['CLASS_HEALTH'][0]}-{STAT_RANGES['CLASS_HEALTH'][1]}",
    "base_attack": "number between {STAT_RANGES['CLASS_ATTACK'][0]}-{STAT_RANGES['CLASS_ATTACK'][1]}",
    "base_defense": "number between {STAT_RANGES['CLASS_DEFENSE'][0]}-{STAT_RANGES['CLASS_DEFENSE'][1]}",
    "base_mana": "number between {STAT_RANGES['CLASS_MANA'][0]}-{STAT_RANGES['CLASS_MANA'][1]}",
    "skills": [
        {{
            "name": "primary offensive skill name",
            "damage": "number between {STAT_RANGES['SKILL_DAMAGE'][0]}-{STAT_RANGES['SKILL_DAMAGE'][1]}",
            "mana_cost": "number between {STAT_RANGES['SKILL_MANA_COST'][0]}-{STAT_RANGES['SKILL_MANA_COST'][1]}",
            "description": "dark-themed skill effect"
        }},
        {{
            "name": "secondary utility skill name",
            "damage": "number between {STAT_RANGES['SKILL_DAMAGE'][0]}-{STAT_RANGES['SKILL_DAMAGE'][1]}",
            "mana_cost": "number between {STAT_RANGES['SKILL_MANA_COST'][0]}-{STAT_RANGES['SKILL_MANA_COST'][1]}",
            "description": "dark-themed utility effect"
        }}
    ]
}}"""

    content = generate_content(prompt)
    if not content:
        return None

    try:
        data = json.loads(content)
        # Validate and normalize stats
        stats = {
            "base_health": (
                STAT_RANGES["CLASS_HEALTH"][0],
                STAT_RANGES["CLASS_HEALTH"][1],
            ),
            "base_attack": (
                STAT_RANGES["CLASS_ATTACK"][0],
                STAT_RANGES["CLASS_ATTACK"][1],
            ),
            "base_defense": (
                STAT_RANGES["CLASS_DEFENSE"][0],
                STAT_RANGES["CLASS_DEFENSE"][1],
            ),
            "base_mana": (STAT_RANGES["CLASS_MANA"][0], STAT_RANGES["CLASS_MANA"][1]),
        }

        for stat, (min_val, max_val) in stats.items():
            data[stat] = max(min_val, min(max_val, int(data[stat])))

        # Process skills
        skills = []
        for skill in data["skills"]:
            skill_data = {
                "name": str(skill["name"]),
                "damage": max(
                    STAT_RANGES["SKILL_DAMAGE"][0],
                    min(STAT_RANGES["SKILL_DAMAGE"][1], int(skill["damage"])),
                ),
                "mana_cost": max(
                    STAT_RANGES["SKILL_MANA_COST"][0],
                    min(STAT_RANGES["SKILL_MANA_COST"][1], int(skill["mana_cost"])),
                ),
                "description": str(skill["description"]),
            }
            skills.append(Skill(**skill_data))

        return CharacterClass(**{**data, "skills": skills})
    except Exception as e:
        print(f"\nError processing character class: {e}")
        return None


def generate_enemy() -> Optional[Enemy]:
    prompt = """Create a dark fantasy enemy with these guidelines:
- Should fit a dark fantasy setting
- Stats must be balanced for player combat
- Can be undead, corrupted, or otherworldly

Return as JSON:
{
    "name": "enemy name",
    "health": "number between 30-100",
    "attack": "number between 8-25",
    "defense": "number between 2-10",
    "exp": "number between 20-100",
    "gold": "number between 10-100"
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

        return Enemy(**data)
    except Exception as e:
        print(f"\nError processing enemy: {e}")
        return None
