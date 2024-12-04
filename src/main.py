#!/usr/bin/env python3

import os
import random
from typing import List
from dotenv import load_dotenv
from src.services.ai_generator import generate_character_class, generate_enemy
from src.services.combat import combat
from src.services.shop import Shop
from src.display.main.main_view import GameView
from src.display.inventory.inventory_view import InventoryView
from src.display.character.character_view import CharacterView
from src.display.combat.combat_view import CombatView
from src.display.shop.shop_view import ShopView
from src.display.base.base_view import BaseView
from src.display.common.message_view import MessageView
from src.config.settings import GAME_BALANCE, STARTING_INVENTORY
from src.models.character import Player, get_fallback_enemy
from src.models.character_classes import CharacterClass, fallback_classes
from src.utils.ascii_art import ensure_character_art
from src.config.logging_config import setup_logging
from src.utils.debug import debug


def get_available_classes(count: int = 3) -> List[CharacterClass]:
    """Generate unique character classes with fallback system"""
    classes = []
    used_names = set()
    max_attempts = 3

    for _ in range(max_attempts):
        try:
            char_class = generate_character_class()
            if char_class and char_class.name not in used_names:
                MessageView.show_success(f"Successfully generated: {char_class.name}")
                if hasattr(char_class, "art") and char_class.art:
                    print("\n" + char_class.art + "\n")
                classes.append(char_class)
                used_names.add(char_class.name)
                if len(classes) >= count:
                    return classes
        except Exception as e:
            MessageView.show_error(f"Attempt failed: {e}")
            break

    if len(classes) < count:
        MessageView.show_info("Using fallback character classes...")
        for c in fallback_classes:
            if len(classes) < count and c.name not in used_names:
                classes.append(c)
                used_names.add(c.name)

    return classes


def main():
    """Main game loop"""
    setup_logging()
    load_dotenv()

    # Initialize views
    game_view = GameView()
    inventory_view = InventoryView()
    character_view = CharacterView()
    combat_view = CombatView()
    shop_view = ShopView()
    base_view = BaseView()

    # Character creation
    character_view.show_character_creation()
    player_name = input().strip()

    classes = get_available_classes()
    character_view.show_class_selection(classes)

    try:
        choice = int(input("\nChoose your class (1-3): ")) - 1
        if 0 <= choice < len(classes):
            chosen_class = classes[choice]
            character_view.show_character_class(chosen_class)
        else:
            MessageView.show_error("Invalid class choice!")
            return
    except ValueError:
        MessageView.show_error("Please enter a valid number!")
        return

    # Initialize player
    player = Player(player_name, chosen_class)
    for item_name, quantity in STARTING_INVENTORY.items():
        player.inventory[item_name] = quantity

    # Initialize shop
    shop = Shop()

    # Main game loop
    while player.health > 0:
        game_view.show_main_status(player)
        choice = input().strip()

        if choice == "1":
            enemy = generate_enemy() or get_fallback_enemy()
            combat(player, enemy, combat_view)
            input("\nPress Enter to continue...")

        elif choice == "2":
            while True:
                base_view.clear_screen()
                shop_view.show_shop_menu(shop, player)
                shop_choice = input().strip()

                if shop_choice == "1":
                    try:
                        item_index = int(input("Enter item number to buy: ")) - 1
                        shop.buy_item(player, item_index)
                    except ValueError:
                        MessageView.show_error("Invalid choice!")
                elif shop_choice == "2":
                    inventory_view.show_inventory(player)
                    try:
                        item_index = int(input("Enter item number to sell: ")) - 1
                        if item_index >= 0:
                            shop.sell_item(player, item_index)
                    except ValueError:
                        MessageView.show_error("Invalid choice!")
                elif shop_choice == "3":
                    break

        elif choice == "3":
            healing = player.rest()
            base_view.display_meditation_effects(healing)

        elif choice == "4":
            inventory_view.show_equipment_management(player)

        elif choice == "5":
            MessageView.show_info("\nThank you for playing! See you next time...")
            break

    if player.health <= 0:
        game_view.show_game_over(player)


if __name__ == "__main__":
    main()
