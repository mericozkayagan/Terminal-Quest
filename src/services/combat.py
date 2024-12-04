from typing import Optional, List
from ..models.character import Player, Enemy
from ..models.items import Item
from ..utils.display import type_text, clear_screen
from ..config.settings import GAME_BALANCE, DISPLAY_SETTINGS
import random
import time
from ..utils.ascii_art import load_ascii_art, display_ascii_art


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
        messages.append(f"{character.name} is affected by {effect_name}")
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


def combat(player: Player, enemy: Enemy) -> bool:
    """
    Handles combat between player and enemy.
    Returns True if player wins, False if player runs or dies.
    """
    clear_screen()
    type_text(f"\nA wild {enemy.name} appears!")

    # Display ASCII art for enemy
    enemy_art = load_ascii_art(f"data/art/{enemy.name.lower().replace(' ', '_')}.txt")
    if enemy_art:
        display_ascii_art(enemy_art)

    time.sleep(DISPLAY_SETTINGS["COMBAT_MESSAGE_DELAY"])

    while enemy.health > 0 and player.health > 0:
        # Process status effects at the start of turn
        effect_messages = process_status_effects(player)
        effect_messages.extend(process_status_effects(enemy))
        for msg in effect_messages:
            type_text(msg)

        print(f"\n{'-'*40}")
        print(f"{enemy.name} HP: {enemy.health}")
        print(f"Your HP: {player.health}/{player.max_health}")
        print(f"Your MP: {player.mana}/{player.max_mana}")

        # Show active status effects
        if player.status_effects:
            effects = [
                f"{name}({effect.duration})"
                for name, effect in player.status_effects.items()
            ]
            print(f"Status Effects: {', '.join(effects)}")

        print(f"\nWhat would you like to do?")
        print("1. Attack")
        print("2. Use Skill")
        print("3. Use Item")
        print("4. Try to Run")

        choice = input("\nYour choice (1-4): ")

        if choice == "1":
            # Basic attack
            damage = calculate_damage(player, enemy, 0)
            enemy.health -= damage
            type_text(f"\nYou deal {damage} damage to the {enemy.name}!")

        elif choice == "2":
            # Skill usage
            print("\nChoose a skill:")
            for i, skill in enumerate(player.skills, 1):
                print(
                    f"{i}. {skill.name} (Damage: {skill.damage}, Mana: {skill.mana_cost})"
                )
                print(f"   {skill.description}")

            try:
                skill_choice = int(input("\nYour choice: ")) - 1
                if 0 <= skill_choice < len(player.skills):
                    skill = player.skills[skill_choice]
                    if player.mana >= skill.mana_cost:
                        damage = calculate_damage(player, enemy, skill.damage)
                        enemy.health -= damage
                        player.mana -= skill.mana_cost
                        type_text(f"\nYou used {skill.name} and dealt {damage} damage!")
                    else:
                        type_text("\nNot enough mana!")
                        continue
            except ValueError:
                type_text("\nInvalid choice!")
                continue

        elif choice == "3":
            # Item usage
            if not player.inventory["items"]:
                type_text("\nNo items in inventory!")
                continue

            print("\nChoose an item to use:")
            for i, item in enumerate(player.inventory["items"], 1):
                print(f"{i}. {item.name}")
                print(f"   {item.description}")

            try:
                item_choice = int(input("\nYour choice: ")) - 1
                if 0 <= item_choice < len(player.inventory["items"]):
                    item = player.inventory["items"][item_choice]
                    if item.use(player):
                        player.inventory["items"].pop(item_choice)
                        type_text(f"\nUsed {item.name}!")
                    else:
                        type_text("\nCannot use this item!")
                        continue
            except ValueError:
                type_text("\nInvalid choice!")
                continue

        elif choice == "4":
            # Try to run
            if random.random() < GAME_BALANCE["RUN_CHANCE"]:
                type_text("\nYou successfully ran away!")
                return False
            else:
                type_text("\nCouldn't escape!")

        # Enemy turn
        if enemy.health > 0:
            damage = calculate_damage(enemy, player, 0)
            player.health -= damage
            type_text(f"The {enemy.name} deals {damage} damage to you!")

    if enemy.health <= 0:
        type_text(f"\nYou defeated the {enemy.name}!")
        player.exp += enemy.exp
        player.inventory["Gold"] += enemy.gold
        type_text(f"You gained {enemy.exp} EXP and {enemy.gold} Gold!")

        # Check for item drops
        dropped_item = check_for_drops(enemy)
        if dropped_item:
            player.inventory["items"].append(dropped_item)
            type_text(f"The {enemy.name} dropped a {dropped_item.name}!")

        # Level up check
        if player.exp >= player.exp_to_level:
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
            type_text(f"\n🎉 Level Up! You are now level {player.level}!")
            time.sleep(DISPLAY_SETTINGS["LEVEL_UP_DELAY"])
        return True

    return False
