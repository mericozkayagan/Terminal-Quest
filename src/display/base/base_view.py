import time
from typing import Dict, Any
from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.themes.dark_theme import DECORATIONS as dec
import os


class BaseView:
    """Base class for all view components"""

    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def display_error(message: str):
        """Display error message"""
        print(f"\n{dec['SEPARATOR']}")
        print(f"  ⚠ {message}")
        print(f"{dec['SEPARATOR']}")

    @staticmethod
    def display_meditation_effects(healing: int):
        """Display meditation/rest effects"""
        BaseView.clear_screen()
        print(f"\n{dec['TITLE']['PREFIX']}Rest{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")
        print("\nYou take a moment to rest...")
        print(f"  {sym['HEALTH']} Health restored: {healing}")
        print(f"  {sym['MANA']} Mana recharged")
        print("\nYour dark powers are refreshed...")
        time.sleep(1.5)
