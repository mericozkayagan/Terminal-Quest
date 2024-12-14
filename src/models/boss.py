from dataclasses import dataclass
from typing import List, Optional, Dict
from src.models.item_sets import ItemSet
from src.models.character import Enemy
from src.models.effects.base import BaseEffect
from src.models.skills import Skill


@dataclass
class BossRequirement:
    min_turns: int = 0
    min_player_level: int = 1
    required_items: List[str] = None
    exploration_chance: float = 0.05


@dataclass
class Boss(Enemy):
    title: str
    associated_set: ItemSet
    requirements: BossRequirement
    special_effects: List[BaseEffect]
    skills: List[Skill]
    rage_threshold: float = 0.3
    current_phase: int = 1

    def __init__(
        self,
        name: str,
        level: int,
        health: int,
        mana: int,
        attack: int,
        defense: int,
        exp_reward: int,
        title: str,
        description: str,
        associated_set: ItemSet,
        requirements: BossRequirement,
        special_effects: List[BaseEffect],
        skills: List[Skill],
        art: str = None,
        rage_threshold: float = 0.3,
    ):
        # Initialize Enemy base class
        super().__init__(
            name=name,
            level=level,
            health=health,
            attack=attack,
            defense=defense,
            exp_reward=exp_reward,
            description=description,
            art=art,
        )

        # Initialize Boss-specific attributes
        self.max_health = health
        self.mana = mana
        self.title = title
        self.associated_set = associated_set
        self.requirements = requirements
        self.special_effects = special_effects
        self.skills = skills
        self.rage_threshold = rage_threshold
        self.current_phase = 1
        self.is_boss = True
        self.guaranteed_drops = [self.associated_set]

    def update_cooldowns(self):
        """Update cooldowns at end of turn"""
        for skill in self.skills:
            skill.update_cooldown()

    def get_priority_skill(self, current_hp_percentage: float) -> Optional[Skill]:
        """Get the highest priority available skill based on situation"""
        # Rage phase check
        if current_hp_percentage <= self.rage_threshold and self.current_phase == 1:
            self.current_phase = 2
            # Prioritize rage skill if available
            rage_skill = self.skills[-1]  # Last skill is rage skill
            if rage_skill.is_available():
                rage_skill.use()
                return self._empower_skill(rage_skill)

        # Normal phase logic
        for skill in self.skills:
            if skill.is_available():
                skill.use()
                return skill

        return None  # No skills available

    def _empower_skill(self, skill: Skill) -> Skill:
        """Enhance skill for rage phase"""
        return Skill(
            name=f"Empowered {skill.name}",
            damage=int(skill.damage * 1.5),
            mana_cost=int(skill.mana_cost * 0.7),
            description=f"Rage-enhanced: {skill.description}",
            cooldown=3,  # Rage skills have longer cooldown
        )


__all__ = ["Boss", "BossRequirement"]
