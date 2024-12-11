from typing import Dict, Optional, List, TYPE_CHECKING
from .base import BaseEffect
from ..base_types import EffectType, EffectTrigger
import random

if TYPE_CHECKING:
    from ..character import Character


class StatModifierEffect(BaseEffect):
    def __init__(
        self,
        stat_name: str,
        modifier: int,
        duration: int = -1,
        is_percentage: bool = False,
    ):
        name = f"{stat_name.title()} {'Boost' if modifier > 0 else 'Reduction'}"
        description = f"{'Increases' if modifier > 0 else 'Decreases'} {stat_name} by {modifier}{'%' if is_percentage else ''}"

        super().__init__(
            name=name,
            description=description,
            effect_type=EffectType.STAT_MODIFIER,
            trigger=EffectTrigger.PASSIVE,
            duration=duration,
        )

        self.stat_name = stat_name
        self.modifier = modifier
        self.is_percentage = is_percentage

    def apply(self, target: "Character", source: Optional["Character"] = None) -> Dict:
        if self.is_percentage:
            base_value = getattr(target, self.stat_name)
            modifier = int(base_value * (self.modifier / 100))
        else:
            modifier = self.modifier

        setattr(target, self.stat_name, getattr(target, self.stat_name) + modifier)
        return {"success": True, "message": self.description}

    def remove(self, target: "Character") -> Dict:
        if self.is_percentage:
            base_value = getattr(target, self.stat_name)
            modifier = int(base_value * (self.modifier / 100))
        else:
            modifier = self.modifier

        setattr(target, self.stat_name, getattr(target, self.stat_name) - modifier)
        return {"success": True, "message": f"Removed {self.name}"}


class OnHitEffect(BaseEffect):
    def __init__(
        self, name: str, description: str, effect: BaseEffect, proc_chance: float = 0.2
    ):
        super().__init__(
            name=name,
            description=description,
            effect_type=EffectType.ITEM_TRIGGER,
            trigger=EffectTrigger.ON_HIT,
            duration=-1,
        )
        self.proc_chance = proc_chance
        self.effect = effect

    def apply(self, target: "Character", source: Optional["Character"] = None) -> Dict:
        if random.random() < self.proc_chance:
            result = self.effect.apply(target, source)
            return {
                "proc": True,
                "effect_applied": True,
                "message": f"{self.name} triggered: {result['message']}",
            }
        return {"proc": False}


class LifestealEffect(BaseEffect):
    def __init__(self, heal_percent: float = 0.2):
        super().__init__(
            name="Lifesteal",
            description=f"Heal for {int(heal_percent * 100)}% of damage dealt",
            effect_type=EffectType.ITEM_TRIGGER,
            trigger=EffectTrigger.ON_HIT,
            duration=-1,
        )
        self.heal_percent = heal_percent

    def apply(
        self, target: "Character", source: Optional["Character"], damage: int = 0
    ) -> Dict:
        if source and damage > 0:
            heal_amount = int(damage * self.heal_percent)
            source.health = min(source.max_health, source.health + heal_amount)
            return {
                "healing": heal_amount,
                "message": f"Lifesteal heals for {heal_amount}",
            }
        return {"healing": 0}


class ShadowLifestealEffect(BaseEffect):
    def __init__(self, heal_percent: float = 0.15):
        super().__init__(
            name="Shadow Lifesteal",
            description=f"Drain {int(heal_percent * 100)}% of damage dealt as health",
            effect_type=EffectType.ITEM_TRIGGER,
            trigger=EffectTrigger.ON_HIT,
            duration=-1,
        )
        self.heal_percent = heal_percent

    def apply(
        self, target: "Character", source: Optional["Character"], damage: int = 0
    ) -> Dict:
        if source and damage > 0:
            heal_amount = int(damage * self.heal_percent)
            source.health = min(source.max_health, source.health + heal_amount)
            return {
                "healing": heal_amount,
                "message": f"Shadow Lifesteal heals for {heal_amount}",
            }
        return {"healing": 0}


class VoidShieldEffect(BaseEffect):
    def __init__(self, block_chance: float = 0.2):
        super().__init__(
            name="Void Shield",
            description=f"{int(block_chance * 100)}% chance to negate damage",
            effect_type=EffectType.ITEM_TRIGGER,
            trigger=EffectTrigger.ON_HIT_TAKEN,
            duration=-1,
        )
        self.block_chance = block_chance

    def apply(
        self, target: "Character", source: Optional["Character"], damage: int = 0
    ) -> Dict:
        if random.random() < self.block_chance:
            return {"blocked": True, "message": f"Void Shield absorbs the attack!"}
        return {"blocked": False}


class HopeBaneEffect(BaseEffect):
    def __init__(self):
        super().__init__(
            name="Hopebane",
            description="Attacks have a chance to inflict despair",
            effect_type=EffectType.ITEM_TRIGGER,
            trigger=EffectTrigger.ON_HIT,
            duration=-1,
        )


class VoidAbsorptionEffect(BaseEffect):
    def __init__(self, proc_chance: float = 0.25):
        super().__init__(
            name="Void Absorption",
            description="Absorb incoming damage to strengthen defenses",
            effect_type=EffectType.ITEM_TRIGGER,
            trigger=EffectTrigger.ON_HIT_TAKEN,
            duration=-1,
        )
        self.proc_chance = proc_chance

    def apply(
        self, target: "Character", source: Optional["Character"], damage: int = 0
    ) -> Dict:
        if random.random() < self.proc_chance:
            defense_boost = min(damage // 4, 5)  # Cap at 5 defense
            target.defense += defense_boost
            return {
                "absorbed": True,
                "defense_boost": defense_boost,
                "message": f"Void Absorption increases defense by {defense_boost}",
            }
        return {"absorbed": False}


class ShadowStrikeEffect(BaseEffect):
    def __init__(self):
        super().__init__(
            name="Shadow Strike",
            description="Attacks from stealth deal increased damage",
            effect_type=EffectType.ITEM_TRIGGER,
            trigger=EffectTrigger.ON_HIT,
            duration=-1,
        )

    def apply(
        self, target: "Character", source: Optional["Character"], damage: int = 0
    ) -> Dict:
        bonus_damage = int(damage * 0.3)
        target.health -= bonus_damage
        return {
            "bonus_damage": bonus_damage,
            "message": f"Shadow Strike deals {bonus_damage} additional damage",
        }


class VoidBoltEffect(BaseEffect):
    def __init__(self, proc_chance: float = 0.2):
        super().__init__(
            name="Void Bolt",
            description="Channel void energy through attacks",
            effect_type=EffectType.ITEM_TRIGGER,
            trigger=EffectTrigger.ON_HIT,
            duration=-1,
        )
        self.proc_chance = proc_chance

    def apply(
        self, target: "Character", source: Optional["Character"], damage: int = 0
    ) -> Dict:
        if random.random() < self.proc_chance:
            void_damage = int(source.magic_power * 0.5)
            target.health -= void_damage
            return {
                "void_damage": void_damage,
                "message": f"Void Bolt strikes for {void_damage} damage",
            }
        return {"void_damage": 0}


class HopesCorruptionEffect(BaseEffect):
    def __init__(self, proc_chance: float = 0.3):
        super().__init__(
            name="Hope's Corruption",
            description="Corrupt enemies with false hope",
            effect_type=EffectType.ITEM_TRIGGER,
            trigger=EffectTrigger.ON_HIT,
            duration=3,
        )
        self.proc_chance = proc_chance

    def apply(
        self, target: "Character", source: Optional["Character"], damage: int = 0
    ) -> Dict:
        if random.random() < self.proc_chance:
            defense_reduction = 15
            target.defense -= defense_reduction
            return {
                "corrupted": True,
                "defense_reduction": defense_reduction,
                "message": f"{target.name} is corrupted, losing {defense_reduction} defense",
            }
        return {"corrupted": False}
