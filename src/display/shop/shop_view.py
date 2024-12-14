from ..common.message_view import MessageView
from ..inventory import inventory_view
from src.models.character import Player
from src.services.shop import SHOP_SETTINGS, Shop
from ..base.base_view import BaseView
from ..themes.dark_theme import SYMBOLS as sym
from ..themes.dark_theme import DECORATIONS as dec
from src.models.items.consumable import Consumable
import random


class ShopView(BaseView):
    """Handles all shop-related display logic"""

    @staticmethod
    def show_shop_menu(shop: Shop, player: Player):
        """Display shop menu with categorized items"""
        print(f"\n{dec['TITLE']['PREFIX']}Dark Market{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        # Show player's gold
        print(
            f"\n{dec['SECTION']['START']}Your Gold: {player.inventory['Gold']}{dec['SECTION']['END']}"
        )

        # Initialize item counter
        item_count = 1

        # Show potions first
        potions = [item for item in shop.inventory if isinstance(item.item, Consumable)]
        if potions:
            print(f"\n{dec['SECTION']['START']}Potions{dec['SECTION']['END']}")
            for shop_item in potions:
                rune = random.choice(dec["RUNES"])
                quantity_str = (
                    f" x{shop_item.quantity}" if shop_item.quantity > 1 else ""
                )
                price = shop.get_item_price(shop_item.item)

                print(f"\n  {rune} [{item_count}] {shop_item.item.name}{quantity_str}")
                print(f"    {sym['GOLD']} Price: {price}")
                print(f"    {sym['INFO']} {shop_item.item.description}")
                if hasattr(shop_item.item, "healing"):
                    print(f"    {sym['HEALTH']} Healing: {shop_item.item.healing}")
                if hasattr(shop_item.item, "mana_restore"):
                    print(f"    {sym['MANA']} Mana: {shop_item.item.mana_restore}")
                print(f"    {sym['INFO']} Rarity: {shop_item.item.rarity.value}")
                item_count += 1

        # Show equipment
        equipment = [
            item for item in shop.inventory if not isinstance(item.item, Consumable)
        ]
        if equipment:
            print(
                f"\n{dec['SECTION']['START']}Equipment & Items{dec['SECTION']['END']}"
            )
            for shop_item in equipment:
                rune = random.choice(dec["RUNES"])
                quantity_str = (
                    f" x{shop_item.quantity}" if shop_item.quantity > 1 else ""
                )
                price = shop.get_item_price(shop_item.item)

                print(f"\n  {rune} [{item_count}] {shop_item.item.name}{quantity_str}")
                print(f"    {sym['GOLD']} Price: {price}")
                print(f"    {sym['INFO']} {shop_item.item.description}")
                if hasattr(shop_item.item, "stat_modifiers"):
                    mods = [
                        f"{stat}: {value}"
                        for stat, value in shop_item.item.stat_modifiers.items()
                    ]
                    print(f"    {sym['ATTACK']} Stats: {', '.join(mods)}")
                print(f"    {sym['INFO']} Rarity: {shop_item.item.rarity.value}")
                item_count += 1

        # Show actions
        print(f"\n{dec['SECTION']['START']}Actions{dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} 1. Buy Item")
        print(f"  {sym['CURSOR']} 2. Sell Item")
        print(
            f"  {sym['CURSOR']} 3. Refresh Shop ({SHOP_SETTINGS['REFRESH_COST']} gold)"
        )
        print(f"  {sym['CURSOR']} 4. Leave Shop")

        print(f"\n{dec['SECTION']['START']}Command{dec['SECTION']['END']}")
        print(f"  {sym['RUNE']} Enter your choice (1-4): ", end="")

    @staticmethod
    def show_buy_prompt():
        """Display the buy prompt with theme"""
        print(f"\n{dec['SECTION']['START']}Purchase{dec['SECTION']['END']}")
        print(f"  {sym['RUNE']} Enter item number to buy (0 to cancel): ", end="")

    @staticmethod
    def show_quantity_prompt(max_quantity: int):
        """Display the quantity prompt with theme"""
        print(f"\n{dec['SECTION']['START']}Quantity{dec['SECTION']['END']}")
        print(
            f"  {sym['RUNE']} Enter quantity (1-{max_quantity}, 0 to cancel): ", end=""
        )

    @staticmethod
    def show_sell_prompt():
        """Display the sell prompt with theme"""
        print(f"\n{dec['SECTION']['START']}Sale{dec['SECTION']['END']}")
        print(f"  {sym['RUNE']} Enter item number to sell (0 to cancel): ", end="")

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

    @staticmethod
    def handle_shop_interaction(shop: Shop, player: Player):
        """Handle all shop-related user interactions"""
        while True:
            BaseView.clear_screen()
            ShopView.show_shop_menu(shop, player)
            shop_choice = input().strip()

            if shop_choice == "1":  # Buy
                print(f"\n{dec['SECTION']['START']}Purchase{dec['SECTION']['END']}")
                try:
                    item_index = (
                        int(
                            input(
                                f"  {sym['RUNE']} Enter item number to buy (0 to cancel): "
                            )
                        )
                        - 1
                    )
                    if item_index >= -1:  # -1 because we subtracted 1 from input
                        if item_index == -1:  # User entered 0
                            continue
                        shop.buy_item(player, item_index)
                    input(f"\n{sym['INFO']} Press Enter to continue...")
                except ValueError:
                    MessageView.show_error("Invalid choice!")
                    input(f"\n{sym['INFO']} Press Enter to continue...")

            elif shop_choice == "2":  # Sell
                inventory_view.show_inventory(player)
                try:
                    item_index = (
                        int(
                            input(
                                f"\n{sym['RUNE']} Enter item number to sell (0 to cancel): "
                            )
                        )
                        - 1
                    )
                    if item_index >= -1:
                        if item_index == -1:  # User entered 0
                            continue
                        if len(player.inventory["items"]) > item_index:
                            shop.sell_item(player, item_index, 1)
                    input(f"\n{sym['INFO']} Press Enter to continue...")
                except ValueError:
                    MessageView.show_error("Invalid choice!")
                    input(f"\n{sym['INFO']} Press Enter to continue...")

            elif shop_choice == "3":  # Refresh
                if shop.refresh_inventory(player):
                    MessageView.show_success("Shop inventory refreshed!")
                input(f"\n{sym['INFO']} Press Enter to continue...")

            elif shop_choice == "4":  # Leave
                break
