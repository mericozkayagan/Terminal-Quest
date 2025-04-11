import logging
import time
from typing import Dict, List, Optional, Any, Tuple

from src.config.database import init_database
from src.display.common.message_view import MessageView
from src.display.save.save_view import SaveView
from src.models.character import Player
from src.services.character_storage import CharacterStorageService

logger = logging.getLogger(__name__)


class SaveManager:
    """Service to manage game saves"""

    # Class variable to track if save system is available
    save_system_available = False

    @staticmethod
    def initialize():
        """Initialize the database for save functionality"""
        logger.info("Initializing save system")
        try:
            init_result = init_database()
            if not init_result:
                logger.error("Failed to initialize save system")
                SaveManager.save_system_available = False
                return False

            # Test database connection
            save_slots = CharacterStorageService.get_save_slots()
            if save_slots is None:
                logger.error("Database connection test failed")
                SaveManager.save_system_available = False
                return False

            logger.info("Save system initialized successfully")
            SaveManager.save_system_available = True
            return True
        except Exception as e:
            logger.error(f"Error initializing save system: {str(e)}")
            SaveManager.save_system_available = False
            return False

    @staticmethod
    def handle_autosave(player: Player, slot_number: int) -> bool:
        """Quietly save the game without user interaction"""
        try:
            # Check if save system is available
            if not SaveManager.save_system_available:
                return False

            # Get save slots to check if the slot exists
            save_slots = CharacterStorageService.get_save_slots()
            if save_slots is None:
                return False

            # Find the selected slot
            selected_slot = None
            for slot in save_slots:
                if slot["slot_number"] == slot_number:
                    selected_slot = slot
                    break

            if not selected_slot:
                return False

            # Save the character (always overwrite on autosave)
            return CharacterStorageService.save_character(player, slot_number)

        except Exception as e:
            logger.error(f"Error in autosave: {str(e)}")
            return False

    @staticmethod
    def handle_save_game(
        player: Player, default_slot: int = 1
    ) -> Tuple[bool, Optional[int]]:
        """Handle save game flow

        Returns:
            Tuple[bool, Optional[int]]: (success, slot_number_used)
        """
        try:
            # Check if save system is available
            if not SaveManager.save_system_available:
                MessageView.show_error("Save system is not available.")
                time.sleep(1.5)
                return False, None

            # Get available save slots
            save_slots = CharacterStorageService.get_save_slots()
            if save_slots is None:
                MessageView.show_error(
                    "Could not connect to the database. Save functionality is unavailable."
                )
                time.sleep(1.5)
                return False, None

            while True:
                # Show save menu
                SaveView.show_save_menu(player, save_slots)

                try:
                    choice = int(input().strip())

                    if choice == 0:  # Back
                        return False, None

                    if 1 <= choice <= 5:
                        # Find the selected slot
                        selected_slot = None
                        for slot in save_slots:
                            if slot["slot_number"] == choice:
                                selected_slot = slot
                                break

                        if not selected_slot:
                            MessageView.show_error("Invalid slot selection")
                            continue

                        # Confirm if overwriting
                        if selected_slot.get(
                            "character_name"
                        ) and not SaveView.confirm_overwrite_save(selected_slot):
                            continue

                        # Save the character
                        if CharacterStorageService.save_character(player, choice):
                            SaveView.show_success()
                            time.sleep(1.5)
                            return True, choice
                        else:
                            SaveView.show_save_error()
                            time.sleep(1.5)
                            return False, None
                    else:
                        MessageView.show_error(
                            "Invalid choice. Please enter a number between 0 and 5."
                        )

                except ValueError:
                    MessageView.show_error("Invalid input. Please enter a number.")

        except Exception as e:
            logger.error(f"Error in save game flow: {str(e)}")
            SaveView.show_save_error()
            time.sleep(1.5)
            return False, None

    @staticmethod
    def handle_load_game() -> Tuple[Optional[Player], Optional[int]]:
        """Handle load game flow

        Returns:
            Tuple[Optional[Player], Optional[int]]: (loaded_player, slot_number)
        """
        try:
            # Check if save system is available
            if not SaveManager.save_system_available:
                MessageView.show_error("Save system is not available.")
                time.sleep(1.5)
                return None, None

            # Get available save slots
            save_slots = CharacterStorageService.get_save_slots()
            if save_slots is None:
                MessageView.show_error(
                    "Could not connect to the database. Load functionality is unavailable."
                )
                time.sleep(1.5)
                return None, None

            while True:
                # Show load menu
                SaveView.show_load_menu(save_slots)

                try:
                    choice = int(input().strip())

                    if choice == 0:  # Back
                        return None, None

                    if 1 <= choice <= 5:
                        # Check if slot has a character
                        has_character = False
                        for slot in save_slots:
                            if slot["slot_number"] == choice and slot.get(
                                "character_name"
                            ):
                                has_character = True
                                break

                        if not has_character:
                            MessageView.show_error("No saved character in this slot")
                            time.sleep(1.5)
                            continue

                        # Load the character
                        player = CharacterStorageService.load_character(choice)
                        if player:
                            MessageView.show_success(f"Welcome back, {player.name}!")
                            time.sleep(1.5)
                            return player, choice
                        else:
                            SaveView.show_load_error()
                            time.sleep(1.5)
                            continue
                    else:
                        MessageView.show_error(
                            "Invalid choice. Please enter a number between 0 and 5."
                        )

                except ValueError:
                    MessageView.show_error("Invalid input. Please enter a number.")

        except Exception as e:
            logger.error(f"Error in load game flow: {str(e)}")
            SaveView.show_load_error()
            time.sleep(1.5)
            return None, None

    @staticmethod
    def handle_delete_save(slot_number: int) -> bool:
        """Handle delete save flow"""
        try:
            # Check if save system is available
            if not SaveManager.save_system_available:
                MessageView.show_error("Save system is not available.")
                time.sleep(1.5)
                return False

            if not (1 <= slot_number <= 5):
                MessageView.show_error("Invalid slot number")
                return False

            # Get slot info
            save_slots = CharacterStorageService.get_save_slots()
            if save_slots is None:
                MessageView.show_error("Could not connect to the database.")
                time.sleep(1.5)
                return False

            slot_info = None
            for slot in save_slots:
                if slot["slot_number"] == slot_number:
                    slot_info = slot
                    break

            if not slot_info:
                MessageView.show_error("Slot not found")
                return False

            # Check if slot has a character
            if not slot_info.get("character_name"):
                MessageView.show_error("No saved character in this slot")
                return False

            # Delete the save
            if CharacterStorageService.delete_save(slot_number):
                MessageView.show_success("Save deleted successfully")
                return True
            else:
                MessageView.show_error("Failed to delete save")
                return False

        except Exception as e:
            logger.error(f"Error in delete save flow: {str(e)}")
            MessageView.show_error("Failed to delete save")
            return False

    @staticmethod
    def handle_start_menu() -> Tuple[bool, Optional[Player], Optional[int]]:
        """Handle the start menu flow

        Returns:
            Tuple[bool, Optional[Player], Optional[int]]: (should_continue, loaded_player, save_slot)
        """
        try:
            while True:
                SaveView.show_start_menu()

                try:
                    choice = int(input().strip())

                    if choice == 1:  # New Game
                        return (True, None, None)

                    elif choice == 2:  # Load Game
                        if not SaveManager.save_system_available:
                            MessageView.show_error(
                                "Save system is not available. Cannot load games."
                            )
                            time.sleep(2)
                            continue

                        player, slot = SaveManager.handle_load_game()
                        if player:
                            return (True, player, slot)
                        # If no player loaded, stay in start menu

                    elif choice == 3:  # Exit
                        return (False, None, None)

                    else:
                        MessageView.show_error(
                            "Invalid choice. Please enter a number between 1 and 3."
                        )

                except ValueError:
                    MessageView.show_error("Invalid input. Please enter a number.")

        except Exception as e:
            logger.error(f"Error in start menu: {str(e)}")
            return (False, None, None)
