from typing import List
from src.display.common.message_view import MessageView
from src.models.character import Player
from src.display.base.base_view import BaseView
from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.themes.dark_theme import DECORATIONS as dec
import random
from src.models.items.equipment import Equipment
from src.models.items.sets import ITEM_SETS
from src.models.base_types import EffectTrigger
from src.models.effects.base import BaseEffect
from src.models.items.consumable import Consumable
from src.models.items.base import Item


class InventoryView(BaseView):
    """Handles all inventory-related display logic"""

    @staticmethod
    def show_inventory(player: "Player"):
        """Display player inventory with categories"""
        print(f"\n{dec['SECTION']['START']}Inventory{dec['SECTION']['END']}")
        print(f"  {sym['GOLD']} Gold: {player.inventory['Gold']}")

        # Show equipped items
        print(f"\n{dec['SECTION']['START']}Equipped{dec['SECTION']['END']}")
        for slot, item in player.equipment.items():
            if item:
                print(f"\n  {sym['EQUIPMENT']} {slot}: {item.name}")
                print(f"    {sym['INFO']} {item.description}")
                if hasattr(item, "stat_modifiers") and isinstance(
                    item.stat_modifiers, dict
                ):
                    mods = [
                        f"{stat}: {value}"
                        for stat, value in item.stat_modifiers.items()
                    ]
                    print(f"    {sym['ATTACK']} Stats: {', '.join(mods)}")
                print(f"    {sym['INFO']} Rarity: {item.rarity.value}")
            else:
                print(f"  {sym['EQUIPMENT']} {slot}: Empty")

        # Show inventory items
        print(f"\n{dec['SECTION']['START']}Items{dec['SECTION']['END']}")
        if player.inventory["items"]:
            for i, item in enumerate(player.inventory["items"], 1):
                rune = random.choice(dec["RUNES"])
                print(f"\n  {rune} [{i}] {item.name}")
                print(f"    {sym['INFO']} {item.description}")
                if hasattr(item, "stat_modifiers") and isinstance(
                    item.stat_modifiers, dict
                ):
                    mods = [
                        f"{stat}: {value}"
                        for stat, value in item.stat_modifiers.items()
                    ]
                    print(f"    {sym['ATTACK']} Stats: {', '.join(mods)}")
                if isinstance(item, Consumable):
                    if hasattr(item, "healing"):
                        print(f"    {sym['HEALTH']} Healing: {item.healing}")
                    if hasattr(item, "mana_restore"):
                        print(f"    {sym['MANA']} Mana: {item.mana_restore}")
                print(f"    {sym['INFO']} Rarity: {item.rarity.value}")
        else:
            print("\n  No items in inventory")

    @staticmethod
    def _show_item_effects(effects: List[BaseEffect]):
        """Display item effects with appropriate symbols"""
        if not effects:
            return

        print(f"    {sym['INFO']} Effects:")
        for effect in effects:
            trigger_symbols = {
                EffectTrigger.ON_HIT: sym["ATTACK"],
                EffectTrigger.ON_KILL: sym["SKULL"],
                EffectTrigger.ON_HIT: sym["DAMAGE"],
                EffectTrigger.PASSIVE: sym["BUFF"],
            }

            trigger_symbol = trigger_symbols.get(effect.trigger, sym["EFFECT"])

            chance_str = f" ({int(effect.chance * 100)}%)" if effect.chance < 1 else ""
            print(
                f"      {trigger_symbol} {effect.name}: {effect.description}{chance_str}"
            )

    @staticmethod
    def _show_set_info(item: Equipment):
        """Display set bonus information for an item"""
        if item.set_name and item.set_name in ITEM_SETS:
            item_set = ITEM_SETS[item.set_name]
            print(f"    {sym['SET']} Set: {item_set.name}")
            for bonus in item_set.bonuses:
                print(f"      ◇ {bonus.required_pieces} pieces: {bonus.description}")

    @staticmethod
    def show_equipment_management(player: "Player"):
        """Display equipment management screen with enhanced item information"""
        while True:
            BaseView.clear_screen()
            print(
                f"\n{dec['TITLE']['PREFIX']}Equipment Management{dec['TITLE']['SUFFIX']}"
            )
            print(f"{dec['SEPARATOR']}")

            # Show equipped items
            print(f"\n{dec['SECTION']['START']}Equipped{dec['SECTION']['END']}")
            for slot, item in player.equipment.items():
                print(f"\n  {sym['EQUIPMENT']} {slot.title()}:")
                if item:
                    print(f"    {item.name} ({item.rarity.value})")
                    # Show stats
                    mods = [
                        f"{stat}: {value}"
                        for stat, value in item.stat_modifiers.items()
                    ]
                    if mods:
                        print(f"    {sym['STATS']} Stats: {', '.join(mods)}")
                    # Show effects
                    InventoryView._show_item_effects(item.effects)
                    # Show set info
                    InventoryView._show_set_info(item)
                else:
                    print("    Empty")

            # Show active set bonuses
            if player.active_set_bonuses:
                print(
                    f"\n{dec['SECTION']['START']}Active Set Bonuses{dec['SECTION']['END']}"
                )
                for set_name, bonuses in player.active_set_bonuses.items():
                    print(f"\n  {sym['SET']} {set_name}:")
                    for bonus in bonuses:
                        print(f"    ◇ {bonus.description}")
                        if bonus.stat_bonuses:
                            stats = [
                                f"{stat}: +{value}"
                                for stat, value in bonus.stat_bonuses.items()
                            ]
                            print(f"      {sym['STATS']} {', '.join(stats)}")
                        InventoryView._show_item_effects(bonus.effects)

            # Show equippable items
            print(f"\n{dec['SECTION']['START']}Inventory{dec['SECTION']['END']}")
            equippable_items = [
                (i, item)
                for i, item in enumerate(player.inventory["items"], 1)
                if isinstance(item, Equipment)
            ]

            if equippable_items:
                for i, (_, item) in enumerate(equippable_items, 1):
                    rune = random.choice(dec["RUNES"])
                    print(f"\n  {rune} {i}. {item.name} ({item.rarity.value})")
                    # Show stats
                    mods = [
                        f"{stat}: {value}"
                        for stat, value in item.stat_modifiers.items()
                    ]
                    if mods:
                        print(f"    {sym['STATS']} Stats: {', '.join(mods)}")
                    # Show effects
                    InventoryView._show_item_effects(item.effects)
                    # Show set info
                    InventoryView._show_set_info(item)
            else:
                print("\n  No equippable items in inventory")

            # Show actions
            print(f"\n{dec['SECTION']['START']}Actions{dec['SECTION']['END']}")
            print(f"  {sym['CURSOR']} Enter item number to equip")
            print(f"  {sym['CURSOR']} U to unequip")
            print(f"  {sym['CURSOR']} 0 to return")

            choice = input("\nChoice: ").strip().lower()

            if choice == "0":
                break
            elif choice == "u":
                InventoryView._handle_unequip(player)
            else:
                InventoryView._handle_equip(player, choice, equippable_items)

    @staticmethod
    def _handle_equip(player: Player, choice: str, equippable_items: List[tuple]):
        """Handle equipping/unequipping items"""
        try:
            if choice.upper() == "U":
                # Show equipped items for unequipping
                print("\nEquipped Items:")
                for slot, item in player.equipment.items():
                    if item:
                        print(f"{slot}: {item.name}")

                slot = (
                    input("\nEnter slot to unequip (or 0 to cancel): ").strip().lower()
                )
                if slot != "0" and slot in player.equipment:
                    player.unequip_item(slot)
                    MessageView.show_success(f"Unequipped item from {slot}")
            else:
                # Handle equipping
                item_index = int(choice) - 1
                if 0 <= item_index < len(equippable_items):
                    # Get the actual item from the tuple (index, item)
                    _, item = equippable_items[item_index]
                    if player.equip_item(item):
                        MessageView.show_success(f"Equipped {item.name}")
                    else:
                        MessageView.show_error("Cannot equip item")
                else:
                    MessageView.show_error("Invalid item number")
        except ValueError:
            MessageView.show_error("Invalid choice")

    @staticmethod
    def _handle_unequip(player: Player):
        """Handle unequipping items"""
        try:
            # Show equipped items for unequipping
            print("\nEquipped Items:")
            equipped_slots = []
            slot_index = 1

            # Create a mapping of numbers to slots
            slot_mapping = {}
            for slot, item in player.equipment.items():
                if item:
                    equipped_slots.append(slot)
                    slot_mapping[slot_index] = slot
                    print(f"  {slot_index}. {slot}: {item.name}")
                    slot_index += 1

            if not equipped_slots:
                MessageView.show_error("No items equipped!")
                return

            choice = input("\nEnter number to unequip (0 to cancel): ").strip()
            if choice == "0":
                return

            try:
                choice_num = int(choice)
                if choice_num in slot_mapping:
                    slot = slot_mapping[choice_num]
                    if player.unequip_item(slot):
                        MessageView.show_success(f"Unequipped item from {slot}")
                    else:
                        MessageView.show_error("Failed to unequip item")
                else:
                    MessageView.show_error("Invalid choice!")
            except ValueError:
                MessageView.show_error("Please enter a valid number")

        except Exception as e:
            MessageView.show_error(f"Failed to unequip: {str(e)}")
