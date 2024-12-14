import json
from typing import Optional
from enum import Enum
from src.models.items.consumable import Consumable
from src.models.items.common_consumables import get_basic_consumables
from src.models.items.base import Item, ItemType, ItemRarity
from src.models.character import Player
from src.display.common.message_view import MessageView
from ..services.item import ItemService
import random
from dataclasses import dataclass
from typing import List
import psycopg2
from src.config.settings import DATABASE_SETTINGS

class ShopType(Enum):
    GENERAL = "general"
    BLACKSMITH = "blacksmith"  # Weapons and armor
    ALCHEMIST = "alchemist"  # Potions and consumables
    MYSTIC = "mystic"  # Magical items and set pieces


SHOP_SETTINGS = {
    "ITEM_APPEARANCE_CHANCE": 0.3,
    "SELL_MULTIPLIER": 0.5,
    "REFRESH_COST": 100,
    "POST_COMBAT_EQUIPMENT_COUNT": 4,
    "SPECIAL_EVENT_CHANCE": 0.2,
    "SHOP_TYPE_WEIGHTS": {
        ShopType.GENERAL: 0.4,
        ShopType.BLACKSMITH: 0.3,
        ShopType.ALCHEMIST: 0.2,
        ShopType.MYSTIC: 0.1,
    },
    "SHOP_TYPE_BONUSES": {
        ShopType.BLACKSMITH: {"weapon": 1.2, "armor": 1.2},
        ShopType.ALCHEMIST: {"consumable": 0.8, "potion_stock": 3},
        ShopType.MYSTIC: {"set_piece_chance": 1.5},
    },
    "BASE_POTION_STOCK": {
        ShopType.GENERAL: 1,
        ShopType.ALCHEMIST: 3,
        ShopType.MYSTIC: 1,
        ShopType.BLACKSMITH: 1,
    },
    "RARITY_WEIGHTS": {
        ItemRarity.COMMON: 0.40,
        ItemRarity.UNCOMMON: 0.30,
        ItemRarity.RARE: 0.20,
        ItemRarity.EPIC: 0.08,
        ItemRarity.LEGENDARY: 0.02,
    },
    "SET_PIECE_CHANCE": 0.15,
    "LEVEL_SCALING": {
        "RARITY_BOOST": 0.02,  # Per player level
        "LEGENDARY_MIN_LEVEL": 20,
        "EPIC_MIN_LEVEL": 15,
    },
}


class ShopEvent:
    def __init__(self, name: str, discount: float, bonus_stock: int = 0):
        self.name = name
        self.discount = discount
        self.bonus_stock = bonus_stock


SHOP_EVENTS = [
    ShopEvent("Fire Sale", 0.7, 0),
    ShopEvent("Merchant Festival", 0.85, 2),
    ShopEvent("Traveling Merchant", 1.0, 3),
    ShopEvent("Set Item Showcase", 0.9, 1),
]


@dataclass
class ShopItem:
    item: Item
    quantity: int


class Shop:
    def __init__(self):
        self.item_service = ItemService()
        self.shop_type = self._random_shop_type()
        self.current_event: Optional[ShopEvent] = None
        self.inventory: List[ShopItem] = self.generate_shop_inventory()
        self.sell_multiplier = SHOP_SETTINGS["SELL_MULTIPLIER"]
        self.connection = psycopg2.connect(
            dbname=DATABASE_SETTINGS["DB_NAME"],
            user=DATABASE_SETTINGS["DB_USER"],
            password=DATABASE_SETTINGS["DB_PASSWORD"],
            host=DATABASE_SETTINGS["DB_HOST"],
            port=DATABASE_SETTINGS["DB_PORT"],
        )
        self.cursor = self.connection.cursor()

    def _random_shop_type(self) -> ShopType:
        roll = random.random()
        cumulative = 0
        for shop_type, weight in SHOP_SETTINGS["SHOP_TYPE_WEIGHTS"].items():
            cumulative += weight
            if roll <= cumulative:
                return shop_type
        return ShopType.GENERAL

    def _check_for_event(self) -> Optional[ShopEvent]:
        if random.random() < SHOP_SETTINGS["SPECIAL_EVENT_CHANCE"]:
            return random.choice(SHOP_EVENTS)
        return None

    def generate_shop_inventory(self, post_combat: bool = False) -> List[ShopItem]:
        """Generate shop inventory based on shop type and events"""
        self.current_event = self._check_for_event()
        inventory: List[ShopItem] = []

        # Add basic consumables based on shop type
        base_potions = get_basic_consumables()
        potion_stock = SHOP_SETTINGS["BASE_POTION_STOCK"][self.shop_type]

        if potion_stock > 0:
            for potion in base_potions:
                if self.shop_type == ShopType.ALCHEMIST:
                    # Alchemist has all potions
                    inventory.append(ShopItem(item=potion, quantity=potion_stock))
                elif self.shop_type == ShopType.GENERAL:
                    # General shop only has basic health/mana potions
                    if potion.value <= 50:  # Basic potions check
                        inventory.append(ShopItem(item=potion, quantity=potion_stock))
                elif self.shop_type == ShopType.MYSTIC:
                    # Mystic only has mana potions
                    if hasattr(potion, "mana_restore") and potion.mana_restore > 0:
                        inventory.append(ShopItem(item=potion, quantity=potion_stock))

        # Calculate base equipment count
        equipment_count = (
            SHOP_SETTINGS["POST_COMBAT_EQUIPMENT_COUNT"] if post_combat else 5
        )
        if self.current_event:
            equipment_count += self.current_event.bonus_stock

        # Generate equipment based on shop type
        for _ in range(equipment_count):
            item = self._generate_typed_item()
            inventory.append(ShopItem(item=item, quantity=1))

        # Handle set pieces
        set_chance = SHOP_SETTINGS["SET_PIECE_CHANCE"]
        if self.shop_type == ShopType.MYSTIC:
            set_chance *= SHOP_SETTINGS["SHOP_TYPE_BONUSES"][ShopType.MYSTIC][
                "set_piece_chance"
            ]

        if random.random() < set_chance:
            set_piece = self.item_service.generate_random_set_piece(
                self._weighted_rarity_selection()
            )
            if set_piece:
                inventory.append(ShopItem(item=set_piece, quantity=1))

        return inventory

    def _generate_typed_item(self) -> Item:
        """Generate an item appropriate for the shop type"""
        rarity = self._weighted_rarity_selection()

        # Get all available items from ItemService
        all_items = self.item_service.get_all_items()

        # Filter items based on shop type
        if self.shop_type == ShopType.BLACKSMITH:
            valid_types = [ItemType.WEAPON, ItemType.ARMOR]
        elif self.shop_type == ShopType.ALCHEMIST:
            valid_types = [ItemType.CONSUMABLE]
        elif self.shop_type == ShopType.MYSTIC:
            valid_types = [ItemType.ACCESSORY, ItemType.WEAPON]
        else:  # GENERAL
            valid_types = list(ItemType)

        # Filter items by type and rarity
        suitable_items = [
            item
            for item in all_items
            if item.item_type in valid_types and item.rarity == rarity
        ]

        if not suitable_items:
            # Fallback to generate a random item if no suitable items found
            return self.item_service.generate_random_item(
                rarity, random.choice(valid_types)
            )

        return random.choice(suitable_items)

    def get_item_price(self, item: Item) -> int:
        """Calculate item price considering shop type and events"""
        base_price = item.value

        # Apply shop type bonuses
        if self.shop_type in SHOP_SETTINGS["SHOP_TYPE_BONUSES"]:
            bonuses = SHOP_SETTINGS["SHOP_TYPE_BONUSES"][self.shop_type]
            if isinstance(item, Consumable) and "consumable" in bonuses:
                base_price *= bonuses["consumable"]

        # Apply event discounts
        if self.current_event:
            base_price = int(base_price * self.current_event.discount)

        return max(1, int(base_price))

    def post_combat_refresh(self):
        """Refresh shop inventory after combat"""
        self.inventory = self.generate_shop_inventory(post_combat=True)

    def sell_item(
        self, player: Player, inventory_index: int, quantity: int = 1
    ) -> bool:
        """Handle selling items from player inventory"""
        try:
            if 0 <= inventory_index < len(player.inventory["items"]):
                item = player.inventory["items"][inventory_index]

                # Count how many of this item the player has
                item_count = sum(1 for i in player.inventory["items"] if i == item)

                if quantity <= 0 or quantity > item_count:
                    MessageView.show_error(f"Invalid quantity! Available: {item_count}")
                    return False

                # Calculate sell value
                sell_value = int(item.value * self.sell_multiplier) * quantity

                # Remove items and add gold
                removed = 0
                for i in range(len(player.inventory["items"]) - 1, -1, -1):
                    if removed >= quantity:
                        break
                    if player.inventory["items"][i] == item:
                        player.inventory["items"].pop(i)
                        removed += 1

                player.inventory["Gold"] += sell_value
                MessageView.show_success(
                    f"Sold {quantity}x {item.name} for {sell_value} gold"
                )
                return True
            else:
                MessageView.show_error("Invalid item selection!")
        except Exception as e:
            MessageView.show_error(f"Sale failed: {str(e)}")
        return False

    def refresh_inventory(self, player: Player) -> bool:
        """Refresh shop inventory for a cost"""
        if player.inventory["Gold"] >= SHOP_SETTINGS["REFRESH_COST"]:
            player.inventory["Gold"] -= SHOP_SETTINGS["REFRESH_COST"]
            self.inventory = self.generate_shop_inventory()
            MessageView.show_success("Shop inventory refreshed!")
            return True
        else:
            MessageView.show_error(
                f"Not enough gold! Cost: {SHOP_SETTINGS['REFRESH_COST']}"
            )
            return False

    def _weighted_rarity_selection(self) -> ItemRarity:
        """Select rarity based on weights"""
        roll = random.random()
        cumulative = 0
        for rarity, weight in SHOP_SETTINGS["RARITY_WEIGHTS"].items():
            cumulative += weight
            if roll <= cumulative:
                return rarity
        return ItemRarity.COMMON

    def find_item(self, item_name: str) -> Optional[ShopItem]:
        """Find item in inventory by name"""
        return next(
            (
                shop_item
                for shop_item in self.inventory
                if shop_item.item.name == item_name
            ),
            None,
        )

    def add_item(self, item: Item, quantity: int = 1):
        """Add item to shop inventory"""
        existing = self.find_item(item.name)
        if existing:
            existing.quantity += quantity
        else:
            self.inventory.append(ShopItem(item, quantity))

    def buy_item(self, player: Player, item_index: int) -> bool:
        """Handle buying items from shop inventory"""
        try:
            if 0 <= item_index < len(self.inventory):
                shop_item = self.inventory[item_index]
                price = self.get_item_price(shop_item.item)

                if player.inventory["Gold"] >= price:
                    # Remove gold and add item to player inventory
                    player.inventory["Gold"] -= price
                    player.inventory["items"].append(shop_item.item)

                    # Decrease quantity or remove from shop
                    shop_item.quantity -= 1
                    if shop_item.quantity <= 0:
                        self.inventory.pop(item_index)

                    MessageView.show_success(
                        f"Bought {shop_item.item.name} for {price} gold"
                    )
                    return True
                else:
                    MessageView.show_error(f"Not enough gold! Need {price} gold")
            else:
                MessageView.show_error("Invalid item selection!")
        except Exception as e:
            MessageView.show_error(f"Purchase failed: {str(e)}")
        return False

    def save_shop_state(self, player_id: str) -> None:
        """Save the current shop state to the database"""
        shop_state = {
            "shop_type": self.shop_type.value,
            "current_event": self.current_event.name if self.current_event else None,
            "inventory": [
                {"item": item.item.serialize(), "quantity": item.quantity}
                for item in self.inventory
            ],
        }
        shop_state_json = json.dumps(shop_state)
        self.cursor.execute(
            """
            INSERT INTO shop_states (player_id, shop_state)
            VALUES (%s, %s)
            ON CONFLICT (player_id) DO UPDATE
            SET shop_state = EXCLUDED.shop_state
            """,
            (player_id, shop_state_json),
        )
        self.connection.commit()

    def load_shop_state(self, player_id: str) -> None:
        """Load the shop state from the database"""
        self.cursor.execute(
            """
            SELECT shop_state FROM shop_states
            WHERE player_id = %s
            """,
            (player_id,),
        )
        result = self.cursor.fetchone()
        if result:
            shop_state_json = result[0]
            shop_state = json.loads(shop_state_json)
            self.shop_type = ShopType(shop_state["shop_type"])
            self.current_event = (
                ShopEvent(shop_state["current_event"], 1.0)
                if shop_state["current_event"]
                else None
            )
            self.inventory = [
                ShopItem(
                    item=Item.deserialize(item_data["item"]),
                    quantity=item_data["quantity"],
                )
                for item_data in shop_state["inventory"]
            ]

    def close(self):
        """Close the database connection"""
        self.cursor.close()
        self.connection.close()
