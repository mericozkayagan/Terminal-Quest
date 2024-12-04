from dataclasses import dataclass
from typing import Dict, Optional
import random


@dataclass
class StatusEffect:
    name: str
    description: str
    duration: int
    stat_modifiers: Optional[Dict[str, int]] = None
    tick_damage: int = 0
    chance_to_apply: float = 1.0

    def apply(self, target: "Character") -> bool:  # type: ignore
        """Attempts to apply the status effect to a target"""
        if random.random() <= self.chance_to_apply:
            # If same effect exists, refresh duration
            if self.name in target.status_effects:
                target.status_effects[self.name].duration = max(
                    self.duration, target.status_effects[self.name].duration
                )
            else:
                target.status_effects[self.name] = self
                # Apply initial stat modifications
                if self.stat_modifiers:
                    for stat, modifier in self.stat_modifiers.items():
                        current_value = getattr(target, stat, 0)
                        setattr(target, stat, current_value + modifier)
            return True
        return False

    def tick(self, target: "Character"):  # type: ignore
        """Apply the effect for one turn"""
        if self.tick_damage:
            damage = self.tick_damage
            # Status effect damage ignores defense
            target.health -= damage
            return damage
        return 0

    def remove(self, target: "Character"):  # type: ignore
        """Remove the effect and revert any stat changes"""
        if self.stat_modifiers:
            for stat, modifier in self.stat_modifiers.items():
                current_value = getattr(target, stat, 0)
                setattr(target, stat, current_value - modifier)
        target.status_effects.pop(self.name, None)


# Predefined status effects
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

WEAKENED = StatusEffect(
    name="Weakened",
    description="Reduced attack and defense from exhaustion",
    duration=2,
    stat_modifiers={"attack": -3, "defense": -2},
    chance_to_apply=0.8,
)

BURNING = StatusEffect(
    name="Burning",
    description="Taking fire damage over time",
    duration=2,
    tick_damage=7,
    chance_to_apply=0.65,
)

CURSED = StatusEffect(
    name="Cursed",
    description="A dark curse reducing all stats",
    duration=3,
    tick_damage=2,
    stat_modifiers={"attack": -2, "defense": -1, "max_mana": -10},
    chance_to_apply=0.5,
)
