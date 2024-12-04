from typing import List
from ..base.base_view import BaseView
from ..themes.dark_theme import SYMBOLS as sym
from ..themes.dark_theme import DECORATIONS as dec
from src.models.items import Item
import random


class ShopView(BaseView):
    """Handles all shop-related display logic"""

    @staticmethod
    def show_shop_welcome():
        """Display shop welcome message"""
        print(f"\n{dec['TITLE']['PREFIX']}Shop{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")
        print("\nWelcome to the shop!")

    @staticmethod
    def show_inventory(items: List[Item], player_gold: int):
        """Display shop inventory"""
        print(
            f"\n{dec['SECTION']['START']}Your Gold: {player_gold}{dec['SECTION']['END']}"
        )

        print(f"\n{dec['SECTION']['START']}Items for Sale{dec['SECTION']['END']}")
        for i, item in enumerate(items, 1):
            rune = random.choice(dec["RUNES"])
            print(f"\n  {rune} {i}. {item.name}")
            print(f"    {sym['GOLD']} Price: {item.value}")
            if hasattr(item, "stat_modifiers"):
                mods = [
                    f"{stat}: {value}" for stat, value in item.stat_modifiers.items()
                ]
                print(f"    {sym['ATTACK']} Stats: {', '.join(mods)}")
            print(f"    ✧ Rarity: {item.rarity.value}")

    @staticmethod
    def show_transaction_result(success: bool, message: str):
        """Display transaction result"""
        if success:
            print(
                f"\n{dec['SECTION']['START']}Purchase Complete{dec['SECTION']['END']}"
            )
        else:
            print(f"\n{dec['SECTION']['START']}Purchase Failed{dec['SECTION']['END']}")
        print(f"  {message}")
