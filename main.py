#!/usr/bin/env python3

import logging
from dotenv import load_dotenv
from src.models.items import Consumable
from src.config.logging_config import setup_logging
from src.services.character_creation import CharacterCreationService
from src.services.combat import combat, handle_level_up
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
from src.display.themes.dark_theme import DECORATIONS as dec
from src.display.themes.dark_theme import SYMBOLS as sym
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="game.log",
)

logger = logging.getLogger(__name__)


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
        return

    # Initialize inventory
    for item_name, quantity in STARTING_INVENTORY.items():
        player.inventory[item_name] = quantity

    # Initialize shop
    shop = Shop()

    base_view.clear_screen()

    # Main game loop
    while player.health > 0:
        BaseView.clear_screen()
        game_view.show_main_status(player)

        choice = input().strip()

        if choice == "1":  # Explore
            try:
                # Generate enemy with proper level scaling
                enemy = generate_enemy(player.level)
                if not enemy:
                    enemy = get_fallback_enemy(player.level)

                if enemy:
                    combat_result = combat(player, enemy, combat_view)
                    if combat_result is None:  # Player died
                        MessageView.show_error("You have fallen in battle...")
                        time.sleep(2)
                        game_view.show_game_over(player)
                        break
                    elif combat_result:  # Victory
                        exp_gained = enemy.exp_reward
                        player.exp += exp_gained
                        MessageView.show_success(
                            f"Victory! Gained {exp_gained} experience!"
                        )
                        time.sleep(5)

                        if player.exp >= player.exp_to_level:
                            handle_level_up(player)
                    else:  # Retreat
                        MessageView.show_info("You retreat from battle...")
                        time.sleep(2)

            except Exception as e:
                logger.error(f"Error during exploration: {str(e)}")
                MessageView.show_error("Failed to generate encounter")
                continue

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
            while True:
                inventory_view.show_inventory(player)
                print(f"\n{dec['SECTION']['START']}Actions{dec['SECTION']['END']}")
                print(f"  {sym['CURSOR']} 1. Manage Equipment")
                print(f"  {sym['CURSOR']} 2. Use Item")
                print(f"  {sym['CURSOR']} 3. Back")

                inv_choice = input("\nChoose action: ").strip()
                BaseView.clear_screen()

                if inv_choice == "1":
                    inventory_view.show_equipment_management(player)
                elif inv_choice == "2":
                    # Show usable items
                    usable_items = [
                        (i, item)
                        for i, item in enumerate(player.inventory["items"], 1)
                        if isinstance(item, Consumable)
                    ]
                    if usable_items:
                        print("\nUsable Items:")
                        for i, (_, item) in enumerate(usable_items, 1):
                            print(f"  {sym['CURSOR']} {i}. {item.name}")
                        try:
                            item_choice = (
                                int(input("\nChoose item to use (0 to cancel): ")) - 1
                            )
                            if 0 <= item_choice < len(usable_items):
                                idx, item = usable_items[item_choice]
                                if item.use(player):
                                    player.inventory["items"].pop(idx - 1)
                                    MessageView.show_success(f"Used {item.name}")
                        except ValueError:
                            MessageView.show_error("Invalid choice!")
                    else:
                        MessageView.show_info("No usable items in inventory!")
                elif inv_choice == "3":
                    break

        elif choice == "5":
            MessageView.show_info("\nThank you for playing! See you next time...")
            break

    if player.health <= 0:
        game_view.show_game_over(player)


if __name__ == "__main__":
    main()
