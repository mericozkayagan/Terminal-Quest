from typing import Optional, List

from src.display.base.base_view import BaseView
from src.display.inventory import inventory_view
from src.models.character import Player, Enemy, Character
from src.models.items import Item, Consumable
from src.display.combat.combat_view import CombatView
from src.display.common.message_view import MessageView
from src.config.settings import GAME_BALANCE, DISPLAY_SETTINGS
import random
import time
from src.utils.ascii_art import display_ascii_art
from src.display.themes.dark_theme import DECORATIONS as dec
from src.display.themes.dark_theme import SYMBOLS as sym


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


def combat(player: Player, enemy: Enemy, combat_view: CombatView) -> Optional[bool]:
    """Handle combat sequence. Returns:
    - True for victory
    - False for retreat
    - None for death
    """
    combat_log = []

    while enemy.health > 0 and player.health > 0:
        BaseView.clear_screen()
        combat_view.show_combat_status(player, enemy, combat_log)

        choice = input("\nChoose your action: ").strip()

        if choice == "1":  # Attack
            # Calculate damage with some randomization
            player_damage = player.get_total_attack() + random.randint(-2, 2)
            enemy_damage = enemy.attack + random.randint(-1, 1)

            # Apply damage
            enemy.health -= player_damage
            player.health -= enemy_damage

            # Add combat log messages
            combat_log.insert(
                0, f"{sym['ATTACK']} You strike for {player_damage} damage!"
            )
            combat_log.insert(
                0, f"{sym['ATTACK']} {enemy.name} retaliates for {enemy_damage} damage!"
            )

            # Trim log to keep last 5 messages
            combat_log = combat_log[:5]

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

                        # Enemy still gets to attack
                        enemy_damage = enemy.attack + random.randint(-1, 1)
                        player.health -= enemy_damage

                        # Add combat log messages
                        combat_log.insert(
                            0,
                            f"{sym['SKILL']} You cast {skill.name} for {skill_damage} damage!",
                        )
                        combat_log.insert(
                            0, f"{sym['MANA']} Consumed {skill.mana_cost} mana"
                        )
                        combat_log.insert(
                            0,
                            f"{sym['ATTACK']} {enemy.name} retaliates for {enemy_damage} damage!",
                        )
                    else:
                        combat_log.insert(0, f"{sym['MANA']} Not enough mana!")
                else:
                    combat_log.insert(0, "Invalid skill selection!")
            except ValueError:
                combat_log.insert(0, "Invalid input!")

        elif choice == "3":  # Use item
            BaseView.clear_screen()
            combat_view.show_combat_items(player)

            try:
                item_choice = int(input("\nChoose item: ")) - 1
                if item_choice == -1:
                    continue

                usable_items = [
                    (i, item)
                    for i, item in enumerate(player.inventory["items"], 1)
                    if isinstance(item, Consumable)
                ]

                if 0 <= item_choice < len(usable_items):
                    idx, item = usable_items[item_choice]
                    if item.use(player):
                        player.inventory["items"].pop(idx - 1)
                        combat_log.insert(0, f"Used {item.name}")

                        # Enemy still gets to attack
                        enemy_damage = enemy.attack + random.randint(-1, 1)
                        player.health -= enemy_damage
                        combat_log.insert(
                            0,
                            f"{sym['ATTACK']} {enemy.name} retaliates for {enemy_damage} damage!",
                        )
                else:
                    combat_log.insert(0, "Invalid item selection!")
            except ValueError:
                combat_log.insert(0, "Invalid input!")

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

        # Check for death after each action
        if player.health <= 0:
            return None  # Player died

    return enemy.health <= 0  # True for victory, False shouldn't happen here


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
