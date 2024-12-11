from enum import Enum, auto
from typing import Optional, List, Tuple

from src.models.boss import Boss
from src.models.base_types import EffectTrigger
from src.display.base.base_view import BaseView
from src.models.character import Player, Enemy, Character
from src.models.items.base import Item
from src.models.items.consumable import Consumable
from src.display.combat.combat_view import CombatView
from src.display.common.message_view import MessageView
from src.config.settings import GAME_BALANCE, DISPLAY_SETTINGS
import random
import time
from src.display.themes.dark_theme import SYMBOLS as sym
from src.services.shop import Shop
from src.services.boss import BossService


class CombatResult(Enum):
    VICTORY = auto()
    DEFEAT = auto()
    RETREAT = auto()


def calculate_damage(
    attacker: "Character", defender: "Character", base_damage: int
) -> int:
    """Calculate damage considering attack, defense, and trigger effects"""
    # Calculate base damage
    damage = max(
        0, attacker.get_total_attack() + base_damage - defender.get_total_defense()
    )

    # Add randomness
    rand_min, rand_max = GAME_BALANCE["DAMAGE_RANDOMNESS_RANGE"]
    damage += random.randint(rand_min, rand_max)

    # Trigger ON_HIT effects for attacker
    attacker.trigger_effects(EffectTrigger.ON_HIT, defender)

    # Trigger ON_HIT_TAKEN effects for defender
    defender.trigger_effects(EffectTrigger.ON_HIT_TAKEN, attacker)

    return damage


def process_status_effects(character: "Character") -> List[str]:
    """Process all status effects and return messages"""
    messages = []
    character.apply_status_effects()

    for effect_name, effect in character.status_effects.items():
        CombatView.show_status_effect(character, effect_name, effect.tick_damage)
        if effect.tick_damage:
            messages.append(f"{effect_name} deals {effect.tick_damage} damage")
    return messages


def handle_combat_rewards(
    player: Player, enemy: Enemy, shop: Shop
) -> Tuple[int, List[Item]]:
    """Handle post-combat rewards including gold, items, and shop refresh"""
    # Calculate gold reward
    base_gold = enemy.level * GAME_BALANCE["GOLD_PER_LEVEL"]
    gold_reward = random.randint(int(base_gold * 0.8), int(base_gold * 1.2))

    # Add gold to player
    player.inventory["Gold"] += gold_reward

    # Get potential drops using ItemService
    dropped_items = shop.item_service.get_enemy_drops(enemy)

    # Add items to player's inventory
    if dropped_items:
        player.inventory["items"].extend(dropped_items)

    # Refresh shop inventory post-combat
    shop.post_combat_refresh()

    return gold_reward, dropped_items


def combat(
    player: Player, enemy: Enemy, combat_view: CombatView, shop: Shop
) -> Optional[bool]:
    """Handle turn-based combat sequence."""
    combat_log = []
    boss_service = BossService() if isinstance(enemy, Boss) else None

    while enemy.health > 0 and player.health > 0:
        BaseView.clear_screen()
        combat_view.show_combat_status(player, enemy, combat_log)

        choice = input("\nChoose your action: ").strip()
        if choice == "1":  # Attack
            # Calculate damage with some randomization
            player_damage = player.get_total_attack() + random.randint(-2, 2)

            # Apply damage to the enemy
            enemy.health -= player_damage
            combat_log.insert(
                0, f"{sym['ATTACK']} You strike for {player_damage} damage!"
            )
        elif choice == "2":  # Use skill
            BaseView.clear_screen()
            combat_view.show_skills(player)

            try:
                skill_choice = int(input("\nChoose skill (0 to cancel): ")) - 1
                if skill_choice == -1:
                    continue

                if 0 <= skill_choice < len(player.skills):
                    skill = player.skills[skill_choice]
                    if player.mana >= skill.mana_cost:
                        # Calculate and apply skill damage
                        skill_damage = skill.damage + random.randint(-3, 3)
                        enemy.health -= skill_damage
                        player.mana -= skill.mana_cost
                        combat_log.insert(
                            0,
                            f"{sym['SKILL']} You cast {skill.name} for {skill_damage} damage!",
                        )
                        combat_log.insert(
                            0, f"{sym['MANA']} Consumed {skill.mana_cost} mana"
                        )
                    else:
                        combat_log.insert(0, f"{sym['MANA']} Not enough mana!")
                else:
                    combat_log.insert(0, "Invalid skill selection!")
            except ValueError as e:
                combat_log.insert(
                    0, f"Invalid input! Please enter a number. Error: {str(e)}"
                )

        elif choice == "3":  # Use item
            BaseView.clear_screen()
            combat_view.show_combat_items(player)

            try:
                item_choice = int(input("\nChoose item: ")) - 1
                if item_choice == -1:  # User chose to return
                    continue
                usable_items = [
                    item
                    for item in player.inventory["items"]
                    if isinstance(item, Consumable)
                ]
                if 0 <= item_choice < len(usable_items):
                    item = usable_items[item_choice]
                    if item.use(player):
                        # Remove the used item
                        player.inventory["items"].remove(item)
                        combat_log.insert(0, f"Used {item.name}")

                        # Show healing/mana restore effects
                        if item.name == "Health Potion":
                            combat_log.insert(
                                0, f"{sym['HEALTH']} Restored {item.value} health!"
                            )
                        if item.name == "Mana Potion":
                            combat_log.insert(
                                0, f"{sym['MANA']} Restored {item.value} mana!"
                            )
                    else:
                        combat_log.insert(0, "Couldn't use that item right now!")
                else:
                    combat_log.insert(0, "Invalid item selection!")
            except ValueError:
                combat_log.insert(0, "Invalid input!")
            continue  # Ensure the loop continues after using an item

        elif choice == "4":  # Retreat
            escape_chance = 0.7 - (enemy.level * 0.05)
            if random.random() < escape_chance:
                combat_view.show_retreat_attempt(success=True)
                return False  # Successful retreat
            else:
                enemy_damage = enemy.attack + random.randint(1, 3)
                player.health -= enemy_damage
                combat_view.show_retreat_attempt(
                    success=False, damage_taken=enemy_damage, enemy_name=enemy.name
                )
                combat_log.insert(
                    0,
                    f"Failed to escape! {enemy.name} hits you for {enemy_damage} damage!",
                )

        # Check for player death
        if player.health <= 0:
            return None

        BaseView.clear_screen()
        combat_view.show_combat_status(player, enemy, combat_log)

        time.sleep(2)

        # Enemy's turn
        if enemy.health > 0:
            if isinstance(enemy, Boss):
                boss_result = boss_service.handle_boss_turn(enemy, player)
                combat_log.insert(
                    0,
                    f"{sym['SKILL']} {enemy.name} uses {boss_result.skill_used} for {boss_result.damage} damage!",
                )
                player.health -= boss_result.damage
                for effect in boss_result.status_effects:
                    effect.apply(player)
                    combat_log.insert(0, f"{sym['EFFECT']} {effect.description}")
                enemy.update_cooldowns()
            else:
                enemy_damage = enemy.attack + random.randint(-1, 1)
                player.health -= enemy_damage
                combat_log.insert(
                    0,
                    f"{sym['ATTACK']} {enemy.name} attacks for {enemy_damage} damage!",
                )

        # Update skill cooldowns at end of turn
        for skill in player.skills:
            skill.update_cooldown()

    return enemy.health <= 0  # True for victory, False shouldn't happen here


def handle_level_up(player: Player):
    """Handle level up logic and display"""
    player.level += 1
    player.exp -= player.exp_to_level
    player.exp_to_level = int(
        player.exp_to_level * GAME_BALANCE["LEVEL_UP_EXP_MULTIPLIER"]
    )
    player.max_health += GAME_BALANCE["LEVEL_UP_HEALTH_INCREASE"]
    player.health = player.max_health
    player.max_mana += GAME_BALANCE["LEVEL_UP_MANA_INCREASE"]
    player.mana = player.max_mana
    player.attack += GAME_BALANCE["LEVEL_UP_ATTACK_INCREASE"]
    player.defense += GAME_BALANCE["LEVEL_UP_DEFENSE_INCREASE"]
    MessageView.show_success(f"🎉 Level Up! You are now level {player.level}!")
    time.sleep(DISPLAY_SETTINGS["LEVEL_UP_DELAY"])
    CombatView.show_level_up(player)
