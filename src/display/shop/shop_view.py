from typing import List
from ..base.base_view import BaseView
from ..themes.dark_theme import SYMBOLS as sym
from ..themes.dark_theme import DECORATIONS as dec
from src.models.items import Item
import random


class ShopView(BaseView):
    """Handles all shop-related display logic"""

    @staticmethod
    def show_shop_menu(shop, player):
        """Display shop menu"""
        print(f"\n{dec['TITLE']['PREFIX']}Dark Market{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        # Show player's gold
        print(
            f"\n{dec['SECTION']['START']}Your Gold: {player.inventory['Gold']}{dec['SECTION']['END']}"
        )

        # Show shop inventory
        print(f"\n{dec['SECTION']['START']}Available Items{dec['SECTION']['END']}")
        for i, item in enumerate(shop.inventory, 1):
            rune = random.choice(dec["RUNES"])
            print(f"\n  {rune} {i}. {item.name}")
            print(f"    {sym['GOLD']} Price: {item.value}")
            if hasattr(item, "stat_modifiers"):
                mods = [
                    f"{stat}: {value}" for stat, value in item.stat_modifiers.items()
                ]
                print(f"    {sym['ATTACK']} Stats: {', '.join(mods)}")
            print(f"    ✧ Rarity: {item.rarity.value}")

        # Show menu options
        print(f"\n{dec['SECTION']['START']}Actions{dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} 1. Buy")
        print(f"  {sym['CURSOR']} 2. Sell")
        print(f"  {sym['CURSOR']} 3. Leave")

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
