from enum import Enum
from typing import Protocol, Dict, Any, Optional, List
from dataclasses import dataclass


class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"


class ItemRarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"

    @property
    def drop_chance(self) -> float:
        return {
            ItemRarity.COMMON: 0.15,
            ItemRarity.UNCOMMON: 0.10,
            ItemRarity.RARE: 0.05,
            ItemRarity.EPIC: 0.03,
            ItemRarity.LEGENDARY: 0.01,
        }[self]


@dataclass
class EffectResult:
    damage: int
    skill_used: str
    status_effects: List[Any]


class EffectType(Enum):
    STATUS = "status"
    SET_BONUS = "set_bonus"
    ITEM_TRIGGER = "item_trigger"
    STAT_MODIFIER = "stat_modifier"


class EffectTrigger(Enum):
    ON_HIT = "on_hit"
    ON_KILL = "on_kill"
    ON_HIT_TAKEN = "on_hit_taken"
    ON_TURN_START = "on_turn_start"
    ON_TURN_END = "on_turn_end"
    PASSIVE = "passive"


class GameEntity(Protocol):
    """Base protocol for game entities that can have effects"""

    name: str
    description: str
    health: int
    max_health: int
    attack: int
    defense: int
    level: int

    def apply_effect(self, effect: Any) -> EffectResult:
        """Apply an effect to the entity"""
        ...

    def remove_effect(self, effect: Any) -> EffectResult:
        """Remove an effect from the entity"""
        ...

    def get_total_attack(self) -> int:
        """Get total attack including all modifiers"""
        ...

    def get_total_defense(self) -> int:
        """Get total defense including all modifiers"""
        ...

    def trigger_effects(
        self, trigger: "EffectTrigger", target: Optional["GameEntity"] = None
    ) -> List[EffectResult]:
        """Trigger all effects of a specific type"""
        ...

    def update_effects(self) -> List[EffectResult]:
        """Update all active effects (tick duration, remove expired)"""
        ...


@dataclass
class BaseStats:
    """Base stats shared between characters and items"""

    attack: int = 0
    defense: int = 0
    magic_power: int = 0
    speed: int = 0
    max_health: int = 0
    max_mana: int = 0
