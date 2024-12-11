from dataclasses import dataclass, field
from typing import Dict, List
from uuid import uuid4

from ..effects.item_effects import LifestealEffect, OnHitEffect, StatModifierEffect
from .base import ItemRarity
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
    name: str
    description: str
    rarity: ItemRarity
    bonuses: List[SetBonus]
    id: str = field(default_factory=lambda: str(uuid4()))

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


# Void Sentinel Set
VOID_SENTINEL_SET = ItemSet(
    name="Void Sentinel",
    description="Ancient armor forged from crystallized darkness, worn by those who guard against hope's corruption",
    rarity=ItemRarity.LEGENDARY,
    bonuses=[
        SetBonus(
            required_pieces=2,
            stat_bonuses={"defense": 15, "max_health": 25},
            effects=[StatModifierEffect("resistance", 10, is_percentage=True)],
            description="Minor void protection",
        ),
        SetBonus(
            required_pieces=4,
            stat_bonuses={"defense": 30, "max_health": 50},
            effects=[
                OnHitEffect(
                    name="Void Absorption",
                    description="Chance to absorb enemy attacks",
                    effect=StatModifierEffect("defense", 5),
                    proc_chance=0.25,
                )
            ],
            description="Major void protection",
        ),
    ],
)

# Shadow Assassin Set
SHADOW_ASSASSIN_SET = ItemSet(
    name="Shadow Assassin",
    description="Gear worn by those who strike from darkness to silence hope's whispers",
    rarity=ItemRarity.EPIC,
    bonuses=[
        SetBonus(
            required_pieces=2,
            stat_bonuses={"attack": 15, "speed": 10},
            effects=[StatModifierEffect("critical_chance", 5, is_percentage=True)],
            description="Enhanced shadow strikes",
        ),
        SetBonus(
            required_pieces=3,
            stat_bonuses={"attack": 25, "speed": 20},
            effects=[LifestealEffect(heal_percent=0.15)],
            description="Shadow lifesteal",
        ),
    ],
)

# Darkweaver Set
DARKWEAVER_SET = ItemSet(
    name="Darkweaver",
    description="Robes woven from pure darkness, protecting the wearer from hope's taint",
    rarity=ItemRarity.EPIC,
    bonuses=[
        SetBonus(
            required_pieces=2,
            stat_bonuses={"max_mana": 20, "magic_power": 15},
            effects=[StatModifierEffect("mana_regeneration", 2)],
            description="Dark magic enhancement",
        ),
        SetBonus(
            required_pieces=4,
            stat_bonuses={"max_mana": 40, "magic_power": 30},
            effects=[
                OnHitEffect(
                    name="Void Bolt",
                    description="Chance to unleash void energy on hit",
                    effect=StatModifierEffect("magic_power", 10),
                    proc_chance=0.2,
                )
            ],
            description="Major dark magic enhancement",
        ),
    ],
)

# Hope's Bane Set
HOPES_BANE_SET = ItemSet(
    name="Hope's Bane",
    description="Artifacts corrupted by the very essence they fight against",
    rarity=ItemRarity.LEGENDARY,
    bonuses=[
        SetBonus(
            required_pieces=2,
            stat_bonuses={"attack": 20, "magic_power": 20},
            effects=[StatModifierEffect("all_damage", 10, is_percentage=True)],
            description="Minor corruption enhancement",
        ),
        SetBonus(
            required_pieces=4,
            stat_bonuses={"attack": 40, "magic_power": 40},
            effects=[
                OnHitEffect(
                    name="Hope's Corruption",
                    description="Chance to corrupt enemies with false hope",
                    effect=StatModifierEffect("defense", -15),
                    proc_chance=0.3,
                ),
                LifestealEffect(heal_percent=0.2),
            ],
            description="Major corruption enhancement",
        ),
    ],
)

# Export all sets
ITEM_SETS = [VOID_SENTINEL_SET, SHADOW_ASSASSIN_SET, DARKWEAVER_SET, HOPES_BANE_SET]
