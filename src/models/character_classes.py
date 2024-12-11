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

    def __post_init__(self):
        """Validate class attributes after initialization"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Invalid name")
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Invalid description")
        if not isinstance(self.base_health, int) or self.base_health <= 0:
            raise ValueError("Invalid base_health")
        if not isinstance(self.base_mana, int) or self.base_mana <= 0:
            raise ValueError("Invalid base_mana")
        if not isinstance(self.base_attack, int) or self.base_attack <= 0:
            raise ValueError("Invalid base_attack")
        if not isinstance(self.base_defense, int) or self.base_defense < 0:
            raise ValueError("Invalid base_defense")
        if not isinstance(self.skills, list) or len(self.skills) == 0:
            raise ValueError("Invalid skills")
        for skill in self.skills:
            if not isinstance(skill, Skill):
                raise ValueError("Invalid skill type")

    def __str__(self):
        return f"CharacterClass(name={self.name}, health={self.base_health}, mana={self.base_mana}, skills={len(self.skills)})"


def get_default_classes() -> List[CharacterClass]:
    """Return default character classes"""
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
                    name="Spectral Strike",
                    damage=25,
                    mana_cost=20,
                    description="Unleashes a ghostly attack that pierces through defenses",
                    cooldown=1,
                ),
                Skill(
                    name="Soul Drain",
                    damage=20,
                    mana_cost=15,
                    description="Drains the enemy's life force to restore health",
                    cooldown=1,
                ),
            ],
        ),
        CharacterClass(
            name="Doombringer",
            description="A harbinger of destruction wielding forbidden magic",
            base_health=90,
            base_mana=100,
            base_attack=14,
            base_defense=4,
            skills=[
                Skill(
                    name="Chaos Bolt",
                    damage=30,
                    mana_cost=25,
                    description="Unleashes a bolt of pure chaos energy",
                    cooldown=1,
                ),
                Skill(
                    name="Dark Nova",
                    damage=35,
                    mana_cost=30,
                    description="Creates an explosion of dark energy",
                    cooldown=2,
                ),
            ],
        ),
        CharacterClass(
            name="Blood Knight",
            description="A warrior who draws power from blood and sacrifice",
            base_health=120,
            base_mana=60,
            base_attack=18,
            base_defense=7,
            skills=[
                Skill(
                    name="Blood Strike",
                    damage=28,
                    mana_cost=20,
                    description="A powerful strike that draws strength from your own blood",
                    cooldown=1,
                ),
                Skill(
                    name="Crimson Shield",
                    damage=15,
                    mana_cost=15,
                    description="Creates a barrier of crystallized blood",
                    cooldown=0,
                ),
            ],
        ),
    ]
