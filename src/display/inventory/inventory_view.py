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
        BaseView.clear_screen()
        print(f"\n{dec['TITLE']['PREFIX']}Inventory{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        # Character Details section
        print(f"\n{dec['SECTION']['START']}Character Details{dec['SECTION']['END']}")
        if hasattr(player.char_class, "art") and player.char_class.art:
            print(f"\n{player.char_class.art}")

        print(f"\n{dec['SECTION']['START']}Base Stats{dec['SECTION']['END']}")
        print(f"  {sym['HEALTH']} Health    {player.health}/{player.max_health}")
        print(f"  {sym['MANA']} Mana      {player.mana}/{player.max_mana}")
        print(f"  {sym['ATTACK']} Attack    {player.get_total_attack()}")
        print(f"  {sym['DEFENSE']} Defense   {player.get_total_defense()}")

        print(f"\n{dec['SECTION']['START']}Dark Path{dec['SECTION']['END']}")
        print(f"  {player.char_class.description}")

        print(f"\n{dec['SECTION']['START']}Innate Arts{dec['SECTION']['END']}")
        for skill in player.char_class.skills:
            rune = random.choice(dec["RUNES"])
            print(f"\n  {rune} {skill.name}")
            print(f"    {sym['ATTACK']} Power: {skill.damage}")
            print(f"    {sym['MANA']} Cost: {skill.mana_cost}")
            print(f"    {random.choice(dec['RUNES'])} {skill.description}")

        # Equipment section
        print(f"\n{dec['SECTION']['START']}Equipment{dec['SECTION']['END']}")
        for slot, item in player.equipment.items():
            rune = random.choice(dec["RUNES"])
            name = item.name if item else "None"
            print(f"  {rune} {slot.title():<10} {name}")
            if item and hasattr(item, "stat_modifiers"):
                mods = [
                    f"{stat}: {value}" for stat, value in item.stat_modifiers.items()
                ]
                print(f"    {sym['ATTACK']} Stats: {', '.join(mods)}")
                print(
                    f"    {sym['EQUIPMENT']} Durability: {item.durability}/{item.max_durability}"
                )

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
    def show_equipment_management(player: "Player"):
        """Display equipment management screen"""
        while True:
            BaseView.clear_screen()
            print(
                f"\n{dec['TITLE']['PREFIX']}Equipment Management{dec['TITLE']['SUFFIX']}"
            )
            print(f"{dec['SEPARATOR']}")

            # Show current equipment
            print(
                f"\n{dec['SECTION']['START']}Current Equipment{dec['SECTION']['END']}"
            )
            for slot, item in player.equipment.items():
                rune = random.choice(dec["RUNES"])
                name = item.name if item else "None"
                print(f"  {rune} {slot.title():<10} {name}")

            # Show inventory items that can be equipped
            print(f"\n{dec['SECTION']['START']}Available Items{dec['SECTION']['END']}")
            equippable_items = [
                (i, item)
                for i, item in enumerate(player.inventory["items"], 1)
                if hasattr(item, "slot")
            ]

            if equippable_items:
                for i, item in equippable_items:
                    rune = random.choice(dec["RUNES"])
                    print(f"\n  {rune} {i}. {item.name}")
                    if hasattr(item, "stat_modifiers"):
                        mods = [
                            f"{stat}: {value}"
                            for stat, value in item.stat_modifiers.items()
                        ]
                        print(f"    {sym['ATTACK']} Stats: {', '.join(mods)}")
                    print(f"    ✧ Rarity: {item.rarity.value}")
            else:
                print("  No equipment available...")

            # Show actions
            print(f"\n{dec['SECTION']['START']}Actions{dec['SECTION']['END']}")
            print(f"  {sym['CURSOR']} Enter item number to equip")
            print(f"  {sym['CURSOR']} 0 to return")

            choice = input().strip()
            if choice == "0":
                BaseView.clear_screen()
                return

            try:
                item_index = int(choice) - 1
                if 0 <= item_index < len(equippable_items):
                    # Equipment logic here
                    pass
                else:
                    print("\nInvalid item number!")
                    input("Press Enter to continue...")
            except ValueError:
                print("\nInvalid input!")
                input("Press Enter to continue...")
