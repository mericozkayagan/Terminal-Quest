import os
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.display.base.base_view import BaseView
from src.display.themes.dark_theme import DECORATIONS as dec
from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.common.message_view import MessageView
from src.models.character import Player


class SaveView(BaseView):
    """View for save and load screens"""

    @staticmethod
    def show_save_menu(player: Player, save_slots: List[Dict[str, Any]]):
        """Show the save game menu"""
        BaseView.clear_screen()

        print(f"\n{dec['TITLE']['PREFIX']} SAVE GAME {dec['TITLE']['SUFFIX']}")
        print(f"\n{dec['SECTION']['START']} Character {dec['SECTION']['END']}")
        print(f"  Name: {player.name}")
        print(f"  Class: {player.char_class.name}")
        print(f"  Level: {player.level}")

        print(f"\n{dec['SECTION']['START']} Save Slots {dec['SECTION']['END']}")

        for slot in save_slots:
            slot_num = slot["slot_number"]
            slot_status = "Empty"
            slot_details = ""

            if slot.get("character_name"):
                last_saved = datetime.strftime(
                    slot["last_saved_at"], "%Y-%m-%d %H:%M:%S"
                )
                slot_status = f"{slot['character_name']} (Lv.{slot['level']})"
                slot_details = f"Class: {slot['char_class']} | Last saved: {last_saved}"

            print(f"  {sym['CURSOR']} {slot_num}. {slot_status}")
            if slot_details:
                print(f"     {slot_details}")

        print(f"\n  {sym['CURSOR']} 0. Back")
        print(f"\nSelect a slot to save your game (1-5), or 0 to go back:")

    @staticmethod
    def show_load_menu(save_slots: List[Dict[str, Any]]):
        """Show the load game menu"""
        BaseView.clear_screen()

        print(f"\n{dec['TITLE']['PREFIX']} LOAD GAME {dec['TITLE']['SUFFIX']}")
        print(f"\n{dec['SECTION']['START']} Save Slots {dec['SECTION']['END']}")

        has_saves = False
        for slot in save_slots:
            slot_num = slot["slot_number"]

            if slot.get("character_name"):
                has_saves = True
                last_saved = datetime.strftime(
                    slot["last_saved_at"], "%Y-%m-%d %H:%M:%S"
                )
                print(
                    f"  {sym['CURSOR']} {slot_num}. {slot['character_name']} (Lv.{slot['level']})"
                )
                print(f"     Class: {slot['char_class']} | Last saved: {last_saved}")
            else:
                print(f"  {sym['CURSOR']} {slot_num}. Empty")

        print(f"\n  {sym['CURSOR']} 0. Back")

        if has_saves:
            print(f"\nSelect a slot to load (1-5), or 0 to go back:")
        else:
            print(f"\nNo saved games found. Select 0 to go back.")

    @staticmethod
    def show_start_menu():
        """Show the start menu with new/load game options"""
        BaseView.clear_screen()

        # ASCII art title
        title_art = """
        ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
        ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║
           ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
           ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
           ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
           ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝

           ██████╗ ██╗   ██╗███████╗███████╗████████╗
          ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
          ██║   ██║██║   ██║█████╗  ███████╗   ██║
          ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║
          ╚██████╔╝╚██████╔╝███████╗███████║   ██║
           ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝
        """

        print(title_art)
        print(f"\n{dec['SECTION']['START']} Main Menu {dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} 1. New Game")
        print(f"  {sym['CURSOR']} 2. Load Game")
        print(f"  {sym['CURSOR']} 3. Exit")

        print(f"\nEnter your choice (1-3):")

    @staticmethod
    def confirm_overwrite_save(slot_data: Dict[str, Any]) -> bool:
        """Show confirmation dialog for overwriting a save"""
        if not slot_data.get("character_name"):
            return True

        BaseView.clear_screen()
        char_name = slot_data.get("character_name")
        char_level = slot_data.get("level")
        char_class = slot_data.get("char_class")

        print(f"\n{dec['TITLE']['PREFIX']} CONFIRM OVERWRITE {dec['TITLE']['SUFFIX']}")
        print(f"\nYou are about to overwrite the following save:")
        print(f"  Character: {char_name}")
        print(f"  Level: {char_level}")
        print(f"  Class: {char_class}")

        print(f"\nThis action cannot be undone. Are you sure?")
        print(f"  {sym['CURSOR']} 1. Yes, overwrite save")
        print(f"  {sym['CURSOR']} 2. No, cancel")

        while True:
            try:
                choice = int(input("\nEnter your choice (1-2): "))
                if choice == 1:
                    return True
                elif choice == 2:
                    return False
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    @staticmethod
    def show_success():
        """Show save success message"""
        MessageView.show_success("Game saved successfully!")

    @staticmethod
    def show_save_error():
        """Show save error message"""
        MessageView.show_error("Failed to save game! Please try again.")

    @staticmethod
    def show_load_error():
        """Show load error message"""
        MessageView.show_error("Failed to load game! Save file may be corrupted.")
