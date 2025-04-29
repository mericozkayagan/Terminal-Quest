#!/usr/bin/env python3

import logging
from dotenv import load_dotenv
from src.models.items.consumable import Consumable
from src.config.logging_config import setup_logging
from src.services.character_creation import CharacterCreationService
from src.services.combat import combat, handle_combat_rewards, handle_level_up
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
from src.services.boss import BossService
from src.display.boss.boss_view import BossView
from src.services.encounter_handler import EncounterHandler
from src.display.encounter.encounter_view import EncounterView
from src.display.save.save_view import SaveView
from src.services.save_manager import SaveManager
import time
from src.models.base_types import EffectResult

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="game.log",
)

logger = logging.getLogger(__name__)


def handle_effect_result(result: EffectResult) -> None:
    """Handle the result of effect operations"""
    if "message" in result:
        if result.get("error"):
            MessageView.show_error(result["message"])
        elif result.get("success"):
            MessageView.show_success(result["message"])
        else:
            MessageView.show_info(result["message"])

    if "damage" in result:
        CombatView.show_damage(result["damage"])


def main():
    """Main game loop"""
    setup_logging()
    load_dotenv()

    # Display title screen and clear to ensure a fresh start
    BaseView.clear_screen()

    # Initialize save system first
    save_system_initialized = SaveManager.initialize()
    logger.info(f"Save system initialized: {save_system_initialized}")

    # Show start menu and handle selection
    should_continue, loaded_player, save_slot = SaveManager.handle_start_menu()

    if not should_continue:
        logger.info("User chose to exit from start menu")
        return

    # Initialize views and services only after user has chosen to continue
    game_view = GameView()
    inventory_view = InventoryView()
    character_view = CharacterView()
    combat_view = CombatView()
    shop_view = ShopView()
    base_view = BaseView()
    boss_view = BossView()
    encounter_view = EncounterView()
    boss_service = BossService()

    # Player object and save slot
    player = None
    current_save_slot = save_slot

    # If player was loaded from save, use it
    if loaded_player:
        player = loaded_player
        logger.info(f"Loaded player {player.name} from slot {save_slot}")
    else:
        # Character creation flow
        base_view.clear_screen()
        character_view.show_character_creation()
        player_name = input().strip()

        # Use character creation service
        try:
            player = CharacterCreationService.create_character(player_name)
            if not player:
                MessageView.show_error(
                    "Character creation failed: Invalid name provided"
                )
                return
        except ValueError as e:
            MessageView.show_error(f"Character creation failed: {str(e)}")
            return
        except Exception as e:
            MessageView.show_error(
                "An unexpected error occurred during character creation"
            )
            return

    # Initialize encounter handler with player-specific info
    encounter_handler = EncounterHandler()

    # Initialize shop
    shop = Shop()

    base_view.clear_screen()

    # Autosave counter
    encounters_since_save = 0

    # Main game loop
    while player.health > 0:
        BaseView.clear_screen()
        game_view.show_main_status(player)

        choice = input().strip()

        if choice == "1":  # Explore
            try:
                # Use the encounter handler to manage all exploration encounters
                explore_result = encounter_handler.handle_exploration(
                    player, combat_view, boss_view, shop
                )

                if not explore_result:  # Player died
                    game_view.show_game_over(player)
                    break

                # Show transition between encounters
                EncounterView.show_encounter_transition()

                # Increment autosave counter and save every 3 encounters if save system available
                encounters_since_save += 1
                if (
                    encounters_since_save >= 3
                    and SaveManager.save_system_available
                    and current_save_slot
                ):
                    SaveManager.handle_autosave(player, current_save_slot)
                    encounters_since_save = 0
                    logger.info(f"Autosaved game to slot {current_save_slot}")

            except Exception as e:
                logger.error(f"Error during exploration: {str(e)}")
                MessageView.show_error("Failed to generate encounter")
                continue

        elif choice == "2":  # Shop
            shop_view.handle_shop_interaction(shop, player)

        elif choice == "3":  # Rest
            healing = player.rest()
            base_view.display_meditation_effects(healing)

        elif choice == "4":  # Inventory/Equipment
            while True:
                inventory_view.show_inventory(player)
                print(f"\n{dec['SECTION']['START']}Actions{dec['SECTION']['END']}")
                print(f"  {sym['CURSOR']} 1. Manage Equipment")
                print(f"  {sym['CURSOR']} 2. Use Item")
                print(f"  {sym['CURSOR']} 3. Save Game")
                print(f"  {sym['CURSOR']} 4. Back")

                inv_choice = input("\nChoose action: ").strip()
                BaseView.clear_screen()

                if inv_choice == "1":  # Manage Equipment
                    inventory_view.show_equipment_management(player)
                elif inv_choice == "2":  # Use Item
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
                elif inv_choice == "3":  # Save Game
                    success, slot = SaveManager.handle_save_game(
                        player, current_save_slot or 1
                    )
                    if success and slot:
                        current_save_slot = slot
                        encounters_since_save = 0
                elif inv_choice == "4":  # Back
                    break

        elif choice == "5":  # Exit
            # Offer to save before exiting if save system is available
            if SaveManager.save_system_available:
                print(
                    f"\n{dec['SECTION']['START']}Save before exit?{dec['SECTION']['END']}"
                )
                print(f"  {sym['CURSOR']} 1. Yes, save game")
                print(f"  {sym['CURSOR']} 2. No, exit without saving")
                save_choice = input().strip()

                if save_choice == "1":
                    success, slot = SaveManager.handle_save_game(
                        player, current_save_slot or 1
                    )
                    if success:
                        MessageView.show_info("\nGame saved. Thank you for playing!")
                    else:
                        MessageView.show_info("\nSave failed. Exiting anyway.")

            MessageView.show_info("\nThank you for playing! See you next time...")
            break

        # NEW: Handle facing the boss
        elif choice == "6":
            # Check if boss is actually ready
            boss_progress = encounter_handler.encounter_service.get_boss_progress()
            if boss_progress and boss_progress["encounters_until_boss"] <= 0:
                logger.info("Player chose to face the corruption.")
                # Call the boss encounter handler directly
                alive = encounter_handler._handle_boss_encounter(
                    player, combat_view, boss_view, shop
                )
                if not alive:
                    game_view.show_game_over(player)
                    break  # Exit main loop if player died to boss
                else:
                    # Reset boss counter after encounter (whether won or retreated)
                    encounter_handler.encounter_service.reset_boss_counter()
                    logger.info("Boss counter reset after encounter.")
            else:
                MessageView.show_error("The corruption is not yet fully manifest.")
                time.sleep(1.5)

    if player.health <= 0:
        game_view.show_game_over(player)


if __name__ == "__main__":
    main()
