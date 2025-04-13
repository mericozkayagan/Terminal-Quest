#!/usr/bin/env python3

import logging
import time
import sys
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
from src.services.save_manager import SaveManager
from src.display.save.save_view import SaveView
import time
from src.models.base_types import EffectResult

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="game.log",
)

logger = logging.getLogger(__name__)

# Global variable to track the last save slot used
LAST_SAVE_SLOT = 1


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


def autosave(player: Player) -> None:
    """Automatically save the game using the last used slot"""
    global LAST_SAVE_SLOT
    if SaveManager.save_system_available:
        # Don't show any UI for autosave, just do it silently
        if SaveManager.handle_autosave(player, LAST_SAVE_SLOT):
            logger.info(f"Game autosaved to slot {LAST_SAVE_SLOT}")
        else:
            logger.error(f"Failed to autosave game to slot {LAST_SAVE_SLOT}")


def main():
    """Main game loop"""
    global LAST_SAVE_SLOT
    setup_logging()
    load_dotenv()

    # Initialize save system
    try:
        save_system_available = SaveManager.initialize()
        if not save_system_available:
            MessageView.show_error(
                "Save system initialization failed. The game will run without save functionality."
            )
            time.sleep(2)
    except Exception as e:
        logger.error(f"Save system initialization error: {str(e)}")
        MessageView.show_error(
            "Failed to initialize save system. Game will run without save functionality."
        )
        time.sleep(2)

    # Initialize views
    game_view = GameView()
    inventory_view = InventoryView()
    character_view = CharacterView()
    combat_view = CombatView()
    shop_view = ShopView()
    base_view = BaseView()
    boss_view = BossView()
    boss_service = BossService()

    # Show start menu
    should_continue, loaded_player, save_slot = SaveManager.handle_start_menu()
    if not should_continue:
        MessageView.show_info("Thanks for playing!")
        return

    # Update the last save slot if we loaded a character
    if save_slot:
        LAST_SAVE_SLOT = save_slot

    # Character creation or use loaded player
    player = loaded_player
    if not player:
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
                # Check for boss encounter first
                boss = boss_service.check_boss_encounter(player)
                if boss:
                    boss_view.show_boss_encounter(boss)
                    combat_result = combat(player, boss, combat_view, shop)

                    if combat_result is False:  # Player died
                        MessageView.show_info("You have fallen to a mighty foe...")
                        time.sleep(2)
                        game_view.show_game_over(player)
                        break
                    elif combat_result:  # Victory
                        exp_gained = int(
                            boss.level * GAME_BALANCE["exp_multiplier"] * 2
                        )
                        player.exp += exp_gained
                        MessageView.show_success(
                            f"A mighty victory! Gained {exp_gained} experience!"
                        )

                        # Handle boss drops
                        for item in boss.guaranteed_drops:
                            player.inventory["items"].append(item)
                            MessageView.show_success(f"Obtained {item.name}!")

                        if player.exp >= player.exp_to_level:
                            handle_level_up(player)

                        # Autosave after boss encounter
                        autosave(player)
                        time.sleep(5)
                    else:  # Retreat
                        MessageView.show_info("You retreat from the powerful foe...")
                        time.sleep(2)
                    continue  # Skip normal enemy generation after boss encounter

                # Generate enemy with proper level scaling
                enemy = generate_enemy(player.level)
                if not enemy:
                    enemy = get_fallback_enemy(player.level)

                if enemy:
                    combat_result = combat(player, enemy, combat_view, shop)
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
                        time.sleep(4)

                        # Handle combat rewards
                        gold_gained, dropped_items = handle_combat_rewards(
                            player, enemy, shop
                        )

                        # Display rewards
                        rewards = {
                            "exp": exp_gained,
                            "gold": gold_gained,
                            "items": dropped_items,
                        }
                        combat_view.show_battle_result(player, enemy, rewards)

                        if player.exp >= player.exp_to_level:
                            handle_level_up(player)

                        # Autosave after successful combat
                        autosave(player)
                    else:  # Retreat
                        MessageView.show_info("You retreat from battle...")
                        time.sleep(2)

            except Exception as e:
                logger.error(f"Error during exploration: {str(e)}")
                MessageView.show_error("Failed to generate encounter")
                continue

        elif choice == "2":  # Shop
            shop_view.handle_shop_interaction(shop, player)
            # Autosave after shopping
            autosave(player)

        elif choice == "3":  # Rest
            healing = player.rest()
            base_view.display_meditation_effects(healing)
            # Autosave after resting
            autosave(player)

        elif choice == "4":  # Inventory
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
                    # Autosave after equipment changes
                    autosave(player)
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
                                    # Autosave after using items
                                    autosave(player)
                        except ValueError:
                            MessageView.show_error("Invalid choice!")
                    else:
                        MessageView.show_info("No usable items in inventory!")
                elif inv_choice == "3":
                    break

        elif choice == "5":  # Save Game
            if not SaveManager.save_system_available:
                MessageView.show_error("Save system is not available.")
                time.sleep(1.5)
            else:
                # Pass in the last used slot as the default
                success, slot_used = SaveManager.handle_save_game(
                    player, LAST_SAVE_SLOT
                )
                if success and slot_used:
                    LAST_SAVE_SLOT = slot_used

        elif choice == "6":  # Exit
            # Prompt for saving before exit
            if SaveManager.save_system_available:
                MessageView.show_info(
                    "Do you want to save your game before exiting? (y/n)"
                )
                save_choice = input().strip().lower()
                if save_choice == "y":
                    success, slot_used = SaveManager.handle_save_game(
                        player, LAST_SAVE_SLOT
                    )
                    if success and slot_used:
                        LAST_SAVE_SLOT = slot_used

            MessageView.show_info("\nThank you for playing! See you next time...")
            break

    if player.health <= 0:
        game_view.show_game_over(player)


if __name__ == "__main__":
    main()
