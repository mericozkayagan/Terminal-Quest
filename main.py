#!/usr/bin/env python3

import os
import random
from dotenv import load_dotenv
from src.services.ai_generator import generate_character_class, generate_enemy
from src.services.combat import combat
from src.services.shop import Shop
from src.utils.display import clear_screen, type_text
from src.config.settings import GAME_BALANCE, STARTING_INVENTORY
from src.models.character import Player, get_fallback_enemy
from src.models.character_classes import fallback_classes
from src.utils.ascii_art import (
    convert_pixel_art_to_ascii,
    load_ascii_art,
    display_ascii_art,
)


def generate_unique_classes(count: int = 3):
    """Generate unique character classes with fallback system"""
    classes = []
    used_names = set()
    max_attempts = 3

    # Try to generate classes with API
    for _ in range(max_attempts):
        try:
            char_class = generate_character_class()
            if char_class and char_class.name not in used_names:
                print(f"\nSuccessfully generated: {char_class.name}")
                classes.append(char_class)
                used_names.add(char_class.name)
                if len(classes) >= count:
                    return classes
        except Exception as e:
            print(f"\nAttempt failed: {e}")
            break

    # If we don't have enough classes, use fallbacks
    if len(classes) < count:
        print("\nUsing fallback character classes...")
        for c in fallback_classes:
            if len(classes) < count and c.name not in used_names:
                classes.append(c)
                used_names.add(c.name)

    return classes


def show_stats(player: Player):
    """Display player stats"""
    clear_screen()
    print(f"\n{'='*40}")
    print(
        f"Name: {player.name}  |  Class: {player.char_class.name}  |  Level: {player.level}"
    )
    print(f"Health: {player.health}/{player.max_health}")
    print(f"Mana: {player.mana}/{player.max_mana}")
    print(
        f"Attack: {player.get_total_attack()}  |  Defense: {player.get_total_defense()}"
    )
    print(f"EXP: {player.exp}/{player.exp_to_level}")
    print(f"Gold: {player.inventory['Gold']}")

    # Show equipment
    print("\nEquipment:")
    for slot, item in player.equipment.items():
        if item:
            print(f"{slot.title()}: {item.name}")
        else:
            print(f"{slot.title()}: None")

    # Show inventory
    print("\nInventory:")
    for item in player.inventory["items"]:
        print(f"- {item.name}")
    print(f"{'='*40}\n")

    # Display ASCII art for player
    player_art = load_ascii_art(
        f"data/art/{player.char_class.name.lower().replace(' ', '_')}.txt"
    )
    if player_art:
        display_ascii_art(player_art)


def main():
    # Load environment variables
    load_dotenv()

    clear_screen()
    type_text("Welcome to Terminal Quest! 🗡️", 0.05)
    player_name = input("\nEnter your hero's name: ")

    # Generate or get character classes
    print("\nGenerating character classes...")
    classes = generate_unique_classes(3)

    # Character selection
    print("\nChoose your class:")
    for i, char_class in enumerate(classes, 1):
        print(f"\n{i}. {char_class.name}")
        print(f"   {char_class.description}")
        print(
            f"   Health: {char_class.base_health} | Attack: {char_class.base_attack} | Defense: {char_class.base_defense} | Mana: {char_class.base_mana}"
        )
        print("\n   Skills:")
        for skill in char_class.skills:
            print(
                f"   - {skill.name}: {skill.description} (Damage: {skill.damage}, Mana: {skill.mana_cost})"
            )

    # Class selection input
    while True:
        try:
            choice = int(input("\nYour choice (1-3): ")) - 1
            if 0 <= choice < len(classes):
                player = Player(player_name, classes[choice])
                break
        except ValueError:
            pass
        print("Invalid choice, please try again.")

    # Initialize shop
    shop = Shop()

    # Main game loop
    while player.health > 0:
        show_stats(player)
        print("\nWhat would you like to do?")
        print("1. Fight an Enemy")
        print("2. Visit Shop")
        print("3. Rest (Heal 20 HP and 15 MP)")
        print("4. Manage Equipment")
        print("5. Quit Game")

        choice = input("\nYour choice (1-5): ")

        if choice == "1":
            enemy = generate_enemy() or get_fallback_enemy()
            combat(player, enemy)
            input("\nPress Enter to continue...")

        elif choice == "2":
            shop.show_inventory(player)
            while True:
                print("\n1. Buy Item")
                print("2. Sell Item")
                print("3. Leave Shop")
                shop_choice = input("\nYour choice (1-3): ")

                if shop_choice == "1":
                    try:
                        item_index = int(input("Enter item number to buy: ")) - 1
                        shop.buy_item(player, item_index)
                    except ValueError:
                        print("Invalid choice!")
                elif shop_choice == "2":
                    if not player.inventory["items"]:
                        type_text("\nNo items to sell!")
                        continue
                    print("\nYour items:")
                    for i, item in enumerate(player.inventory["items"], 1):
                        print(
                            f"{i}. {item.name} - Worth: {int(item.value * GAME_BALANCE['SELL_PRICE_MULTIPLIER'])} Gold"
                        )
                    try:
                        item_index = int(input("Enter item number to sell: ")) - 1
                        shop.sell_item(player, item_index)
                    except ValueError:
                        print("Invalid choice!")
                elif shop_choice == "3":
                    break

        elif choice == "3":
            healed = False
            if player.health < player.max_health:
                player.health = min(player.max_health, player.health + 20)
                healed = True
            if player.mana < player.max_mana:
                player.mana = min(player.max_mana, player.mana + 15)
                healed = True

            if healed:
                type_text("You rest and recover some health and mana...")
            else:
                type_text("You are already at full health and mana!")

        elif choice == "4":
            # Equipment management
            if not player.inventory["items"]:
                type_text("\nNo items to equip!")
                continue

            print("\nYour items:")
            equippable_items = [
                item for item in player.inventory["items"] if hasattr(item, "equip")
            ]
            if not equippable_items:
                type_text("\nNo equipment items found!")
                continue

            for i, item in enumerate(equippable_items, 1):
                print(f"{i}. {item.name} ({item.item_type.value})")

            try:
                item_index = int(input("\nChoose item to equip (0 to cancel): ")) - 1
                if 0 <= item_index < len(equippable_items):
                    item = equippable_items[item_index]
                    old_item = player.equip_item(item, item.item_type.value)
                    player.inventory["items"].remove(item)
                    if old_item:
                        player.inventory["items"].append(old_item)
                    type_text(f"\nEquipped {item.name}!")
            except ValueError:
                print("Invalid choice!")

        elif choice == "5":
            type_text("\nThanks for playing Terminal Quest! Goodbye! 👋")
            break

    if player.health <= 0:
        type_text("\nGame Over! Your hero has fallen in battle... 💀")
        type_text(f"Final Level: {player.level}")
        type_text(f"Gold Collected: {player.inventory['Gold']}")


if __name__ == "__main__":
    main()
