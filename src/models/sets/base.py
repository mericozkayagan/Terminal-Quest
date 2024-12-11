from dataclasses import dataclass, field
from typing import Dict, List
from uuid import uuid4
from ..items.base import ItemRarity
from ..effects.base import BaseEffect


@dataclass
class SetBonus:
    required_pieces: int
    stat_bonuses: Dict[str, int]
    effects: List[BaseEffect]
    description: str

    def to_dict(self) -> Dict:
        return {
            "required_pieces": self.required_pieces,
            "stat_bonuses": self.stat_bonuses,
            "effects": [effect.to_dict() for effect in self.effects],
            "description": self.description,
        }


@dataclass
class ItemSet:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    rarity: ItemRarity
    bonuses: List[SetBonus]

    def get_active_bonuses(self, equipped_count: int) -> List[SetBonus]:
        return [
            bonus for bonus in self.bonuses if bonus.required_pieces <= equipped_count
        ]

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "rarity": self.rarity.value,
            "bonuses": [bonus.to_dict() for bonus in self.bonuses],
        }
