import json
import logging
import pickle
import base64
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from src.config.database import execute_query
from src.models.character import Player
from src.models.character_classes import get_default_classes, CharacterClass
from src.models.items.equipment import Equipment
from src.models.items.consumable import Consumable
from src.models.items.item import Item
from src.models.base_types import ItemType, ItemRarity

logger = logging.getLogger(__name__)


class CharacterStorageService:
    """Service to handle character storage operations"""

    @staticmethod
    def get_save_slots() -> List[Dict[str, Any]]:
        """Get all save slots with their status"""
        query = """
        SELECT
            ss.slot_number,
            ss.last_saved_at,
            c.id as character_id,
            c.name as character_name,
            c.char_class,
            c.level
        FROM
            save_slots ss
        LEFT JOIN
            characters c ON ss.character_id = c.id
        ORDER BY
            ss.slot_number
        """

        try:
            results = execute_query(query)
            if results is None:
                return []
            return results
        except Exception as e:
            logger.error(f"Error getting save slots: {str(e)}")
            return []

    @staticmethod
    def save_character(player: Player, slot_number: int) -> bool:
        """Save character to a specific slot"""
        try:
            # Start transaction
            conn = None
            from src.config.database import get_connection

            conn = get_connection()
            if not conn:
                logger.error("Failed to get database connection for saving character")
                return False

            cursor = conn.cursor()

            try:
                # Check if character exists in this slot
                cursor.execute(
                    """
                    SELECT character_id FROM save_slots
                    WHERE slot_number = %s
                    """,
                    (slot_number,),
                )
                slot_data = cursor.fetchone()

                # If there's an existing character in this slot, delete it first
                if slot_data and slot_data["character_id"]:
                    cursor.execute(
                        "DELETE FROM characters WHERE id = %s",
                        (slot_data["character_id"],),
                    )

                # Insert character
                cursor.execute(
                    """
                    INSERT INTO characters
                    (name, char_class, level, exp, exp_to_level, health, max_health,
                    attack, defense, mana, max_mana, gold)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        player.name,
                        player.char_class.name,
                        player.level,
                        player.exp,
                        player.exp_to_level,
                        player.health,
                        player.max_health,
                        player.attack,
                        player.defense,
                        player.mana,
                        player.max_mana,
                        player.inventory.get("Gold", 0),
                    ),
                )

                character_id = cursor.fetchone()["id"]

                # Save inventory items
                for item in player.inventory.get("items", []):
                    item_data = {
                        "description": item.description,
                        "value": item.value,
                    }

                    # Add type-specific data
                    if isinstance(item, Equipment):
                        item_data["stat_modifiers"] = item.stat_modifiers
                        item_data["item_type"] = item.item_type.name
                        item_data["set_name"] = item.set_name
                        item_data["rarity"] = (
                            item.rarity.name if hasattr(item, "rarity") else "COMMON"
                        )
                    elif isinstance(item, Consumable):
                        # Only add these fields if they exist on the Consumable object
                        if hasattr(item, "effect_strength"):
                            item_data["effect_strength"] = item.effect_strength
                        if hasattr(item, "effect_type"):
                            item_data["effect_type"] = item.effect_type

                    cursor.execute(
                        """
                        INSERT INTO inventory_items
                        (character_id, item_type, item_name, item_data, equipped, slot)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            character_id,
                            item.__class__.__name__,
                            item.name,
                            json.dumps(item_data),
                            False,
                            None,
                        ),
                    )

                # Save equipped items
                for slot_name, item in player.equipment.items():
                    if item:
                        item_data = {
                            "description": item.description,
                            "value": item.value,
                            "stat_modifiers": item.stat_modifiers,
                            "item_type": item.item_type.name,
                            "set_name": item.set_name,
                            "rarity": (
                                item.rarity.name
                                if hasattr(item, "rarity")
                                else "COMMON"
                            ),
                        }

                        cursor.execute(
                            """
                            INSERT INTO inventory_items
                            (character_id, item_type, item_name, item_data, equipped, slot)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (
                                character_id,
                                "Equipment",
                                item.name,
                                json.dumps(item_data),
                                True,
                                slot_name,
                            ),
                        )

                # Update save slot
                cursor.execute(
                    """
                    UPDATE save_slots
                    SET character_id = %s, last_saved_at = NOW()
                    WHERE slot_number = %s
                    """,
                    (character_id, slot_number),
                )

                conn.commit()
                logger.info(f"Character {player.name} saved to slot {slot_number}")
                return True

            except Exception as e:
                if conn:
                    conn.rollback()
                logger.error(f"Error saving character: {str(e)}")
                return False
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        except Exception as e:
            logger.error(f"Error in save_character: {str(e)}")
            return False

    @staticmethod
    def load_character(slot_number: int) -> Optional[Player]:
        """Load character from a specific slot"""
        try:
            # Get character ID from slot
            slot_query = """
            SELECT character_id FROM save_slots
            WHERE slot_number = %s AND character_id IS NOT NULL
            """

            slot_result = execute_query(slot_query, (slot_number,))
            if not slot_result:
                logger.info(f"No saved character in slot {slot_number}")
                return None

            character_id = slot_result[0]["character_id"]

            # Get character data
            char_query = """
            SELECT * FROM characters WHERE id = %s
            """

            char_result = execute_query(char_query, (character_id,))
            if not char_result:
                logger.error(f"Character {character_id} not found")
                return None

            char_data = char_result[0]

            # Get character class
            char_class_name = char_data["char_class"]
            char_class = None

            # Find matching class from defaults
            for cls in get_default_classes():
                if cls.name == char_class_name:
                    char_class = cls
                    break

            if not char_class:
                logger.error(f"Character class {char_class_name} not found")
                return None

            # Create player instance
            player = Player(name=char_data["name"], char_class=char_class)
            player.level = char_data["level"]
            player.exp = char_data["exp"]
            player.exp_to_level = char_data["exp_to_level"]
            player.health = char_data["health"]
            player.max_health = char_data["max_health"]
            player.attack = char_data["attack"]
            player.defense = char_data["defense"]
            player.mana = char_data["mana"]
            player.max_mana = char_data["max_mana"]
            player.inventory["Gold"] = char_data["gold"]

            # Clear default inventory
            player.inventory["items"] = []

            # Get inventory items
            items_query = """
            SELECT * FROM inventory_items WHERE character_id = %s
            """

            items_result = execute_query(items_query, (character_id,))

            # Process items
            for item_data in items_result:
                from src.models.items.equipment import Equipment
                from src.models.items.consumable import Consumable

                item_type = item_data["item_type"]
                item_name = item_data["item_name"]
                item_json = json.loads(item_data["item_data"])
                is_equipped = item_data["equipped"]
                slot = item_data["slot"]

                # Create item based on type
                item = None

                if item_type == "Equipment":
                    # Convert string item_type to enum
                    type_enum = ItemType[item_json.get("item_type", "WEAPON")]

                    # Convert string rarity to enum if present
                    rarity = None
                    if "rarity" in item_json:
                        rarity = ItemRarity[item_json.get("rarity", "COMMON")]

                    item = Equipment(
                        name=item_name,
                        description=item_json.get("description", ""),
                        value=item_json.get("value", 0),
                        stat_modifiers=item_json.get("stat_modifiers", {}),
                        item_type=type_enum,
                        set_name=item_json.get("set_name"),
                        rarity=rarity,
                    )

                    if is_equipped and slot:
                        player.equipment[slot] = item
                        # Apply equipment stat modifiers
                        for stat, value in item.stat_modifiers.items():
                            current = getattr(player, stat, 0)
                            setattr(player, stat, current + value)
                    else:
                        player.inventory["items"].append(item)

                elif item_type == "Consumable":
                    item = Consumable(
                        name=item_name,
                        description=item_json.get("description", ""),
                        value=item_json.get("value", 0),
                        effect_type=item_json.get("effect_type", "heal"),
                        effect_strength=item_json.get("effect_strength", 10),
                    )
                    player.inventory["items"].append(item)

            logger.info(f"Character {player.name} loaded from slot {slot_number}")
            return player

        except Exception as e:
            logger.error(f"Error loading character: {str(e)}")
            return None

    @staticmethod
    def delete_save(slot_number: int) -> bool:
        """Delete a save from a specific slot"""
        try:
            query = """
            UPDATE save_slots
            SET character_id = NULL, last_saved_at = NOW()
            WHERE slot_number = %s
            RETURNING character_id
            """

            result = execute_query(query, (slot_number,))
            if not result:
                logger.error(f"Failed to update save slot {slot_number}")
                return False

            # If character exists, delete it
            character_id = result[0].get("character_id")
            if character_id:
                delete_query = "DELETE FROM characters WHERE id = %s"
                execute_query(delete_query, (character_id,))

            logger.info(f"Save in slot {slot_number} deleted")
            return True

        except Exception as e:
            logger.error(f"Error deleting save: {str(e)}")
            return False
