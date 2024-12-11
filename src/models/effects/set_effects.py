from dataclasses import dataclass
from typing import Dict, List, Optional

from ...models.effects.item_effects import ShadowLifestealEffect, VoidShieldEffect
from .base import BaseEffect
from ..character import Character
from ..base_types import EffectTrigger, EffectType


@dataclass
class SetEffect(BaseEffect):
    stat_bonuses: Dict[str, int]
    required_pieces: int
    active: bool = False

    def __init__(
        self,
        name: str,
        description: str,
        stat_bonuses: Dict[str, int],
        required_pieces: int,
        effects: List[BaseEffect] = None,
    ):
        super().__init__(
            name=name,
            description=description,
            effect_type=EffectType.SET_BONUS,
            trigger=EffectTrigger.PASSIVE,
            duration=-1,
        )
        self.stat_bonuses = stat_bonuses
        self.required_pieces = required_pieces
        self.bonus_effects = effects or []

    def apply(self, target: Character, source: Optional[Character] = None) -> Dict:
        if not self.active:
            # Apply stat bonuses
            for stat, value in self.stat_bonuses.items():
                current = getattr(target, stat, 0)
                setattr(target, stat, current + value)

            # Apply bonus effects
            for effect in self.bonus_effects:
                effect.apply(target, source)

            self.active = True
            return {"success": True, "message": f"Set bonus '{self.name}' activated!"}
        return {"success": False, "message": "Set bonus already active"}

    def remove(self, target: Character) -> Dict:
        if self.active:
            # Remove stat bonuses
            for stat, value in self.stat_bonuses.items():
                current = getattr(target, stat, 0)
                setattr(target, stat, current - value)

            # Remove bonus effects
            for effect in self.bonus_effects:
                effect.remove(target)

            self.active = False
            return {"success": True, "message": f"Set bonus '{self.name}' deactivated"}
        return {"success": False, "message": "Set bonus not active"}


@dataclass
class VoidwalkerSetEffect(SetEffect):
    def __init__(self):
        super().__init__(
            name="Voidwalker's Embrace",
            description="Harness the power of the void",
            stat_bonuses={"max_health": 30, "defense": 15},
            required_pieces=3,
            effects=[VoidShieldEffect(0.25)],
        )


@dataclass
class ShadowstalkersSetEffect(SetEffect):
    def __init__(self):
        super().__init__(
            name="Shadowstalker's Guile",
            description="Move as one with the shadows",
            stat_bonuses={"attack": 20, "speed": 10},
            required_pieces=4,
            effects=[ShadowLifestealEffect(0.2)],
        )
