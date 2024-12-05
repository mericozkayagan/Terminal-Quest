#!/usr/bin/env python3

import os
from typing import List
from dotenv import load_dotenv
from src.config.logging_config import setup_logging
from src.services.character_creation import CharacterCreationService
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
from src.services.ai_generator import generate_enemy


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

    # Use character creation service
    try:
        player = CharacterCreationService.create_character(player_name)
        if not player:
            MessageView.show_error("Character creation failed: Invalid name provided")
            return
    except ValueError as e:
        MessageView.show_error(f"Character creation failed: {str(e)}")
        return
    except Exception as e:
        MessageView.show_error("An unexpected error occurred during character creation")
        logger.error(f"Character creation error: {str(e)}")
        return

    # Initialize inventory
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
