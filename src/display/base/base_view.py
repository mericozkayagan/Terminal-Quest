import time
from typing import Dict, Any
from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.themes.dark_theme import DECORATIONS as dec
import os
import logging


class BaseView:
    """Base class for all view components"""

    DEBUG_MODE = os.getenv("DEBUG_MODE", False)
    logger = logging.getLogger("display")

    @classmethod
    def initialize(cls, debug_mode: bool = False):
        """Initialize the base view with debug settings"""
        cls.DEBUG_MODE = debug_mode
        cls.logger.debug(f"BaseView initialized with DEBUG_MODE: {debug_mode}")

    @classmethod
    def clear_screen(cls):
        """Clear screen if not in debug mode"""
        if not cls.DEBUG_MODE:
            os.system("cls" if os.name == "nt" else "clear")
        else:
            cls.logger.debug("Screen clear skipped (DEBUG_MODE)")
            print("\n" + "=" * 50 + "\n")  # Visual separator in debug mode

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
        print(f"  {sym['MANA']} Mana recharged: {healing}")
        print("\nYour dark powers are refreshed...")
        time.sleep(1.5)
