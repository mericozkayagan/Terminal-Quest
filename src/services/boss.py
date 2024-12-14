from typing import Optional, List, Dict
from random import random, choice
from src.models.boss_types import BOSS_ENEMIES
from src.models.boss import Boss
from src.models.character import Player
from src.models.skills import Skill
from src.models.base_types import EffectResult


class BossService:
    def __init__(self):
        self.exploration_turns = 0

    def check_boss_encounter(self, player: Player) -> Optional[Boss]:
        """Check if conditions are met for a boss encounter"""
        self.exploration_turns += 1

        for boss in BOSS_ENEMIES:
            try:
                if self._meets_requirements(boss.requirements, player):
                    if (
                        self.exploration_turns >= boss.requirements.min_turns
                        or random() < boss.requirements.exploration_chance
                    ):
                        self.exploration_turns = 0
                        return boss
            except AttributeError as e:
                print(f"Error checking boss requirements: {e}")
        return None

    def _meets_requirements(self, requirements, player: Player) -> bool:
        """Check if player meets boss encounter requirements"""
        try:
            if player.level < requirements.min_player_level:
                return False
            return True
        except AttributeError as e:
            print(f"Error accessing player level or requirements: {e}")
            return False

    def handle_boss_turn(self, boss: Boss, player: Player) -> EffectResult:
        """Handle boss combat turn with special skill logic"""
        try:
            current_hp_percentage = boss.health / boss.max_health
        except ZeroDivisionError as e:
            print(f"Error calculating current HP percentage: {e}")
            current_hp_percentage = 0

        # Get boss action for this turn
        skill = boss.get_priority_skill(current_hp_percentage)

        if skill:
            try:
                # Calculate and apply damage
                damage = self.calculate_boss_damage(skill, boss, player)
                player.health -= damage
                boss.mana -= skill.mana_cost

                return EffectResult(
                    damage=damage,
                    skill_used=skill.name,
                    status_effects=boss.special_effects,
                )
            except Exception as e:
                print(f"Error during boss skill execution: {e}")
                return EffectResult(damage=0, skill_used="Error", status_effects=[])
        else:
            # Basic attack if no skills available
            try:
                damage = boss.attack + random.randint(-2, 2)
                player.health -= damage
                return EffectResult(
                    damage=damage, skill_used="Basic Attack", status_effects=[]
                )
            except Exception as e:
                print(f"Error during boss basic attack: {e}")
                return EffectResult(damage=0, skill_used="Error", status_effects=[])

    def calculate_boss_damage(self, skill: Skill, boss: Boss, player: Player) -> int:
        """Calculate damage for boss skills with proper scaling"""
        try:
            base_damage = skill.damage
            level_scaling = 1 + (boss.level * 0.1)  # 10% increase per level
            attack_scaling = 1 + (boss.attack * 0.02)  # 2% per attack point
            defense_reduction = max(
                0.2, 1 - (player.defense * 0.01)
            )  # Max 80% reduction

            raw_damage = base_damage * level_scaling * attack_scaling
            final_damage = max(int(raw_damage * defense_reduction), 1)

            return final_damage
        except Exception as e:
            print(f"Error calculating boss damage: {e}")
            return 0
