from typing import Optional, List

from src.display.inventory import inventory_view
from ..models.character import Player, Enemy, Character
from ..models.items import Item
from src.display.combat.combat_view import CombatView
from src.display.common.message_view import MessageView
from ..config.settings import GAME_BALANCE, DISPLAY_SETTINGS
import random
import time
from .art_generator import generate_enemy_art
from ..utils.ascii_art import display_ascii_art


def calculate_damage(
    attacker: "Character", defender: "Character", base_damage: int
) -> int:
    """Calculate damage considering attack, defense and randomness"""
    damage = max(
        0, attacker.get_total_attack() + base_damage - defender.get_total_defense()
    )
    rand_min, rand_max = GAME_BALANCE["DAMAGE_RANDOMNESS_RANGE"]
    return damage + random.randint(rand_min, rand_max)


def process_status_effects(character: "Character") -> List[str]:
    """Process all status effects and return messages"""
    messages = []
    character.apply_status_effects()

    for effect_name, effect in character.status_effects.items():
        CombatView.show_status_effect(character, effect_name, effect.tick_damage)
        if effect.tick_damage:
            messages.append(f"{effect_name} deals {effect.tick_damage} damage")

    return messages


def check_for_drops(enemy: Enemy) -> Optional[Item]:
    """Check for item drops from enemy"""
    from ..models.items import (
        RUSTY_SWORD,
        LEATHER_ARMOR,
        HEALING_SALVE,
        POISON_VIAL,
        VAMPIRIC_BLADE,
        CURSED_AMULET,
    )

    possible_drops = [
        RUSTY_SWORD,
        LEATHER_ARMOR,
        HEALING_SALVE,
        POISON_VIAL,
        VAMPIRIC_BLADE,
        CURSED_AMULET,
    ]

    for item in possible_drops:
        if random.random() < item.drop_chance:
            return item
    return None


def combat(player: Player, enemy: Enemy, combat_view: CombatView) -> bool:
    """Handle combat sequence"""
    while enemy.health > 0 and player.health > 0:
        combat_view.show_combat_status(player, enemy)
        choice = input("\nChoose your action: ").strip()

        if choice == "1":
            # Basic attack
            damage = player.get_total_attack()
            enemy.health -= damage
            player.health -= enemy.attack

        elif choice == "2":
            # Use skill
            combat_view.show_skills(player)
            try:
                skill_choice = int(input("\nChoose skill: ")) - 1
                if 0 <= skill_choice < len(player.skills):
                    skill = player.skills[skill_choice]
                    if player.mana >= skill.mana_cost:
                        enemy.health -= skill.damage
                        player.mana -= skill.mana_cost
                        player.health -= enemy.attack
                    else:
                        print("Not enough mana!")
            except ValueError:
                print("Invalid choice!")

        elif choice == "3":
            # Use item
            inventory_view.show_inventory(player)

        elif choice == "4":
            # Retreat
            return False

    # Combat ended
    if enemy.health <= 0:
        rewards = {
            "exp": enemy.exp_reward,
            "gold": enemy.gold_reward,
            "items": enemy.get_drops(),
        }
        combat_view.show_battle_result(player, enemy, rewards)

        # Handle rewards
        player.exp += rewards["exp"]
        player.inventory["Gold"] += rewards["gold"]
        for item in rewards["items"]:
            player.inventory["items"].append(item)

        # Check level up
        if player.check_level_up():
            gains = player.level_up()
            combat_view.show_level_up(player, gains)

        return True

    return False


def handle_level_up(player: Player):
    """Handle level up logic and display"""
    player.level += 1
    player.exp -= player.exp_to_level
    player.exp_to_level = int(
        player.exp_to_level * GAME_BALANCE["LEVEL_UP_EXP_MULTIPLIER"]
    )

    # Increase stats
    player.max_health += GAME_BALANCE["LEVEL_UP_HEALTH_INCREASE"]
    player.health = player.max_health
    player.max_mana += GAME_BALANCE["LEVEL_UP_MANA_INCREASE"]
    player.mana = player.max_mana
    player.attack += GAME_BALANCE["LEVEL_UP_ATTACK_INCREASE"]
    player.defense += GAME_BALANCE["LEVEL_UP_DEFENSE_INCREASE"]

    MessageView.show_success(f"🎉 Level Up! You are now level {player.level}!")
    time.sleep(DISPLAY_SETTINGS["LEVEL_UP_DELAY"])
    CombatView.show_level_up(player)
