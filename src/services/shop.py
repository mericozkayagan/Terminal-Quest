from typing import List, Optional
from ..models.items import Item, generate_random_item
from ..models.character import Player
from src.display.shop.shop_view import ShopView
from src.display.common.message_view import MessageView


class Shop:
    def __init__(self):
        self.inventory: List[Item] = []
        self.refresh_inventory()

    def refresh_inventory(self):
        """Refresh shop inventory with new random items"""
        self.inventory.clear()
        num_items = 5  # Number of items to generate
        for _ in range(num_items):
            item = generate_random_item()
            self.inventory.append(item)

    def show_shop_menu(self, player: Player, shop_view: ShopView):
        """Display shop menu"""
        shop_view.show_shop_welcome()
        shop_view.show_inventory(self.inventory, player.inventory["Gold"])
        print("\nChoose an action:")
        print("1. Buy")
        print("2. Sell")
        print("3. Leave")

    def buy_item(self, player: Player, item_index: int, shop_view: ShopView):
        """Handle item purchase"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if player.inventory["Gold"] >= item.value:
                player.inventory["Gold"] -= item.value
                player.inventory["items"].append(item)
                self.inventory.pop(item_index)
                shop_view.show_transaction_result(True, f"Purchased {item.name}")
            else:
                shop_view.show_transaction_result(False, "Not enough gold!")
        else:
            shop_view.show_transaction_result(False, "Invalid item!")

    def sell_item(self, player: Player, item_index: int, shop_view: ShopView):
        """Handle item sale"""
        if 0 <= item_index < len(player.inventory["items"]):
            item = player.inventory["items"].pop(item_index)
            player.inventory["Gold"] += item.value // 2
            shop_view.show_transaction_result(True, f"Sold {item.name}")
        else:
            shop_view.show_transaction_result(False, "Invalid item!")
