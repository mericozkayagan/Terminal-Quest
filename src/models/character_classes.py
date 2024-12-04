from dataclasses import dataclass
from typing import List
from .skills import Skill


@dataclass
class CharacterClass:
    name: str
    description: str
    base_health: int
    base_mana: int
    base_attack: int
    base_defense: int
    skills: List[Skill]
    art: str = None


def get_default_classes() -> List[CharacterClass]:
    """Return default character classes when AI generation is disabled"""
    return [
        CharacterClass(
            name="Shadow Revenant",
            description="A vengeful spirit bound by darkness",
            base_health=100,
            base_mana=80,
            base_attack=16,
            base_defense=5,
            skills=[
                Skill(
                    "Spectral Strike",
                    25,
                    20,
                    "Unleashes a ghostly attack that pierces through defenses",
                ),
                Skill(
                    "Ethereal Veil",
                    20,
                    15,
                    "Cloaks the Shadow Revenant in mist, reducing incoming damage",
                ),
            ],
        ),
        CharacterClass(
            name="Soul Reaper",
            description="A harvester of souls who grows stronger with each kill",
            base_health=90,
            base_mana=70,
            base_attack=18,
            base_defense=4,
            skills=[
                Skill(
                    "Soul Harvest",
                    30,
                    25,
                    "Drains the enemy's life force to restore health",
                ),
                Skill(
                    "Death's Embrace",
                    22,
                    18,
                    "Surrounds the enemy in dark energy, weakening their defenses",
                ),
            ],
        ),
        CharacterClass(
            name="Plague Herald",
            description="A corrupted physician who weaponizes disease and decay",
            base_health=95,
            base_mana=75,
            base_attack=15,
            base_defense=6,
            skills=[
                Skill(
                    "Virulent Plague",
                    28,
                    22,
                    "Inflicts a devastating disease that spreads to nearby enemies",
                ),
                Skill(
                    "Miasmic Shield",
                    18,
                    15,
                    "Creates a barrier of toxic fumes that damages attackers",
                ),
            ],
        ),
    ]
