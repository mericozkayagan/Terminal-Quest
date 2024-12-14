from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from uuid import uuid4
from ..base_types import GameEntity, EffectTrigger, EffectType
import random


@dataclass
class BaseEffect:
    name: str
    description: str
    effect_type: EffectType
    trigger: EffectTrigger
    duration: int
    chance: float = 1.0
    id: str = field(default_factory=lambda: str(uuid4()))
    potency: float = 1.0
    stack_limit: int = 1

    def apply(
        self, target: GameEntity, source: Optional[GameEntity] = None
    ) -> Dict[str, Any]:
        if random.random() <= self.chance:
            return {"success": True, "message": f"{self.name} applied"}
        else:
            return {"success": False, "message": f"{self.name} failed to apply"}

    def remove(self, target: GameEntity) -> Dict[str, Any]:
        return {"success": True, "message": f"{self.name} removed"}

    def can_stack(self, existing_effect: "BaseEffect") -> bool:
        return self.stack_limit > existing_effect.stack_count

    def combine(self, existing_effect: "BaseEffect") -> bool:
        if self.can_stack(existing_effect):
            existing_effect.potency += self.potency
            existing_effect.stack_count += 1
            return True
        return False

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "effect_type": self.effect_type.value,
            "trigger": self.trigger.value,
            "duration": self.duration,
            "potency": self.potency,
        }
