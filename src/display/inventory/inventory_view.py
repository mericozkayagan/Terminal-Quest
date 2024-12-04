from typing import List, Dict

from src.models.character import Player
from src.display.base.base_view import BaseView
from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.themes.dark_theme import DECORATIONS as dec
from src.models.items import Item
import random


class InventoryView(BaseView):
    """Handles all inventory-related display logic"""

    @staticmethod
    def show_inventory(player: "Player"):
        """Display inventory"""
        print(f"\n{dec['TITLE']['PREFIX']}Inventory{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        # Equipment section
        print(f"\n{dec['SECTION']['START']}Equipment{dec['SECTION']['END']}")
        for slot, item in player.equipment.items():
            rune = random.choice(dec["RUNES"])
            name = item.name if item else "None"
            print(f"  {rune} {slot.title():<10} {name}")

        # Items section
        print(f"\n{dec['SECTION']['START']}Items{dec['SECTION']['END']}")
        if player.inventory["items"]:
            for i, item in enumerate(player.inventory["items"], 1):
                rune = random.choice(dec["RUNES"])
                print(f"\n  {rune} {i}. {item.name}")
                if hasattr(item, "stat_modifiers"):
                    mods = [
                        f"{stat}: {value}"
                        for stat, value in item.stat_modifiers.items()
                    ]
                    print(f"    {sym['ATTACK']} Stats: {', '.join(mods)}")
                if hasattr(item, "durability"):
                    print(
                        f"    {sym['EQUIPMENT']} Durability: {item.durability}/{item.max_durability}"
                    )
                print(f"    ✧ Rarity: {item.rarity.value}")
        else:
            print("  Your inventory is empty...")

    @staticmethod
    def show_equipment_management():
        """Display equipment management options"""
        print(f"\n{dec['SECTION']['START']}Equipment Menu{dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} 1. Equip Item")
        print(f"  {sym['CURSOR']} 2. Unequip Item")
        print(f"  {sym['CURSOR']} 3. Back")
