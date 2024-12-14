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
    players: List[Player], enemies: List[Enemy], combat_view: CombatView, shop: Shop
) -> Optional[bool]:
    """Handle turn-based combat sequence for multiple players and enemies."""
    combat_log = []
    boss_service = (
        BossService() if any(isinstance(enemy, Boss) for enemy in enemies) else None
    )

    # Initialize player and enemy queues
    player_queue = players[:]
    enemy_queue = enemies[:]

    while player_queue and enemy_queue:
        BaseView.clear_screen()
        combat_view.show_combat_status(player_queue, enemy_queue, combat_log)

        # Player's turn
        for player in player_queue:
            if player.health <= 0:
                continue

            choice = input(f"\n{player.name}, choose your action: ").strip()
            if choice == "1":  # Attack
                print("\nChoose your target:")
                for i, enemy in enumerate(enemy_queue):
                    print(f"{i + 1}. {enemy.name} (Health: {enemy.health})")
                try:
                    target_choice = int(input("Enter the number of the target: ")) - 1
                    if 0 <= target_choice < len(enemy_queue):
                        target = enemy_queue[target_choice]
                    else:
                        print("Invalid choice! Targeting a random enemy.")
                        target = random.choice(enemy_queue)
                except ValueError:
                    print("Invalid input! Targeting a random enemy.")
                    target = random.choice(enemy_queue)

                player_damage = calculate_damage(player, target, random.randint(-2, 2))
                target.health -= player_damage
                combat_log.insert(
                    0,
                    f"{sym['ATTACK']} {player.name} strikes {target.name} for {player_damage} damage!",
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
                            print("\nChoose your target:")
                            for i, enemy in enumerate(enemy_queue):
                                print(f"{i + 1}. {enemy.name} (Health: {enemy.health})")
                            try:
                                target_choice = (
                                    int(input("Enter the number of the target: ")) - 1
                                )
                                if 0 <= target_choice < len(enemy_queue):
                                    target = enemy_queue[target_choice]
                                else:
                                    print("Invalid choice! Targeting a random enemy.")
                                    target = random.choice(enemy_queue)
                            except ValueError:
                                print("Invalid input! Targeting a random enemy.")
                                target = random.choice(enemy_queue)

                            skill_damage = calculate_damage(
                                player, target, skill.damage + random.randint(-3, 3)
                            )
                            target.health -= skill_damage
                            player.mana -= skill.mana_cost
                            combat_log.insert(
                                0,
                                f"{sym['SKILL']} {player.name} casts {skill.name} on {target.name} for {skill_damage} damage!",
                            )
                            combat_log.insert(
                                0,
                                f"{sym['MANA']} {player.name} consumed {skill.mana_cost} mana",
                            )
                        else:
                            combat_log.insert(
                                0,
                                f"{sym['MANA']} {player.name} does not have enough mana!",
                            )
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
                            player.inventory["items"].remove(item)
                            combat_log.insert(0, f"{player.name} used {item.name}")

                            if item.name == "Health Potion":
                                combat_log.insert(
                                    0,
                                    f"{sym['HEALTH']} {player.name} restored {item.value} health!",
                                )
                            if item.name == "Mana Potion":
                                combat_log.insert(
                                    0,
                                    f"{sym['MANA']} {player.name} restored {item.value} mana!",
                                )
                        else:
                            combat_log.insert(
                                0, f"{player.name} couldn't use that item right now!"
                            )
                    else:
                        combat_log.insert(0, "Invalid item selection!")
                except ValueError:
                    combat_log.insert(0, "Invalid input!")
                continue

            elif choice == "4":  # Retreat
                escape_chance = 0.7 - (
                    sum(enemy.level for enemy in enemy_queue) / len(enemy_queue) * 0.05
                )
                if random.random() < escape_chance:
                    combat_view.show_retreat_attempt(success=True)
                    return False
                else:
                    enemy_damage = random.choice(enemy_queue).attack + random.randint(
                        1, 3
                    )
                    player.health -= enemy_damage
                    combat_view.show_retreat_attempt(
                        success=False,
                        damage_taken=enemy_damage,
                        enemy_name=random.choice(enemy_queue).name,
                    )
                    combat_log.insert(
                        0,
                        f"Failed to escape! {random.choice(enemy_queue).name} hits {player.name} for {enemy_damage} damage!",
                    )

            if player.health <= 0:
                player_queue.remove(player)

        # Check for player defeat
        if not player_queue:
            return None

        BaseView.clear_screen()
        combat_view.show_combat_status(player_queue, enemy_queue, combat_log)

        time.sleep(2)

        # Enemy's turn
        for enemy in enemy_queue:
            if enemy.health <= 0:
                continue

            if isinstance(enemy, Boss):
                boss_result = boss_service.handle_boss_turn(
                    enemy, random.choice(player_queue)
                )
                combat_log.insert(
                    0,
                    f"{sym['SKILL']} {enemy.name} uses {boss_result.skill_used} for {boss_result.damage} damage!",
                )
                target = random.choice(player_queue)
                target.health -= boss_result.damage
                for effect in boss_result.status_effects:
                    effect.apply(target)
                    combat_log.insert(0, f"{sym['EFFECT']} {effect.description}")
                enemy.update_cooldowns()
            else:
                target = random.choice(player_queue)
                enemy_damage = calculate_damage(enemy, target, random.randint(-1, 1))
                target.health -= enemy_damage
                combat_log.insert(
                    0,
                    f"{sym['ATTACK']} {enemy.name} attacks {target.name} for {enemy_damage} damage!",
                )

            if enemy.health <= 0:
                enemy_queue.remove(enemy)

        # Update skill cooldowns at end of turn
        for player in player_queue:
            for skill in player.skills:
                skill.update_cooldown()

    return not enemy_queue  # True for victory, False for defeat

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
