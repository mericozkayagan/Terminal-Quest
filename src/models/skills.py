from dataclasses import dataclass

@dataclass
class Skill:
    name: str
    damage: int
    mana_cost: int
    description: str