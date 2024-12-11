from typing import Dict, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from .base import BaseEffect
from ..base_types import EffectTrigger, EffectType
import random

if TYPE_CHECKING:
    from ..character import Character


@dataclass
class StatusEffect(BaseEffect):
    stat_modifiers: Dict[str, int] = field(default_factory=dict)
    tick_damage: int = 0
    chance_to_apply: float = 1.0

    def __init__(
        self,
        name: str,
        description: str,
        duration: int,
        stat_modifiers: Optional[Dict[str, int]] = None,
        tick_damage: int = 0,
        chance_to_apply: float = 1.0,
    ):
        super().__init__(
            name=name,
            description=description,
            effect_type=EffectType.STATUS,
            trigger=EffectTrigger.ON_TURN_START,
            duration=duration,
        )
        self.stat_modifiers = stat_modifiers or {}
        self.tick_damage = tick_damage
        self.chance_to_apply = chance_to_apply

    def apply(self, target: "Character", source: Optional["Character"] = None) -> Dict:
        if random.random() <= self.chance_to_apply:
            if self.stat_modifiers:
                for stat, modifier in self.stat_modifiers.items():
                    current_value = getattr(target, stat, 0)
                    setattr(target, stat, current_value + modifier)

            damage = self.tick_damage if self.tick_damage else 0
            if damage:
                target.health -= damage

            return {
                "applied": True,
                "damage": damage,
                "message": f"{self.name} affects {target.name}",
            }
        return {"applied": False}

    def remove(self, target: "Character") -> Dict:
        if self.stat_modifiers:
            for stat, modifier in self.stat_modifiers.items():
                current_value = getattr(target, stat, 0)
                setattr(target, stat, current_value - modifier)
        return {"removed": True}


# Predefined status effects
VOID_EMPOWERED = StatusEffect(
    name="VOID_EMPOWERED",
    description="Empowered by void energy",
    duration=3,
    stat_modifiers={"attack": 5, "magic_power": 8},
)

CORRUPTED_HOPE = StatusEffect(
    name="CORRUPTED_HOPE",
    description="Hope twisted into despair",
    duration=4,
    tick_damage=8,
    stat_modifiers={"defense": -3},
)

BLEEDING = StatusEffect(
    name="Bleeding",
    description="Taking damage over time from blood loss",
    duration=3,
    tick_damage=5,
    chance_to_apply=0.7,
)

POISONED = StatusEffect(
    name="Poisoned",
    description="Taking poison damage and reduced attack",
    duration=4,
    tick_damage=3,
    stat_modifiers={"attack": -2},
    chance_to_apply=0.6,
)

__all__ = ["StatusEffect", "VOID_EMPOWERED", "CORRUPTED_HOPE", "BLEEDING", "POISONED"]
