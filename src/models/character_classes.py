from dataclasses import dataclass
from typing import List
from .skills import Skill

@dataclass
class CharacterClass:
    name: str
    description: str
    base_health: int
    base_attack: int
    base_defense: int
    base_mana: int
    skills: List[Skill]

fallback_classes = [
    CharacterClass(
        name="Plague Herald",
        description="A corrupted physician who weaponizes disease and decay. Masters of pestilence who spread suffering through calculated afflictions.",
        base_health=90,
        base_attack=14,
        base_defense=4,
        base_mana=80,
        skills=[
            Skill(name="Virulent Outbreak", damage=25, mana_cost=20, description="Unleashes a devastating plague that corrupts flesh and spirit"),
            Skill(name="Miasmic Shroud", damage=15, mana_cost=15, description="Surrounds self with toxic vapors that decay all they touch")
        ]
    ),
    CharacterClass(
        name="Blood Sovereign",
        description="A noble cursed with vampiric powers. Sustains their immortality through the essence of others while commanding crimson forces.",
        base_health=100,
        base_attack=16,
        base_defense=5,
        base_mana=70,
        skills=[
            Skill(name="Crimson Feast", damage=28, mana_cost=25, description="Drains life force through cursed bloodletting"),
            Skill(name="Sanguine Storm", damage=20, mana_cost=20, description="Conjures a tempest of crystallized blood shards")
        ]
    ),
    CharacterClass(
        name="Void Harbinger",
        description="A being touched by the cosmic void. Channels the emptiness between stars to unmake reality itself.",
        base_health=85,
        base_attack=12,
        base_defense=3,
        base_mana=100,
        skills=[
            Skill(name="Null Cascade", damage=30, mana_cost=30, description="Tears a rift in space that consumes all it touches"),
            Skill(name="Entropy Surge", damage=22, mana_cost=25, description="Accelerates the decay of matter and spirit")
        ]
    )
]