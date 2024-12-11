from typing import Dict, List
from .base import ItemType, ItemRarity
from ..effects.base import BaseEffect
from ...services.item import ItemService

# WEAPONS
UNCOMMON_WEAPONS = [
    ItemService.create_equipment(
        name="Reinforced Steel Sword",
        description="A finely crafted sword imbued with shadow essence",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"attack": 8},
    ),
    ItemService.create_equipment(
        name="Mystic Staff",
        description="Staff carved from darkwood, resonating with void energy",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"attack": 4, "magic_power": 6},
    ),
    ItemService.create_equipment(
        name="Enhanced War Hammer",
        description="Heavy hammer strengthened with dark iron",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"attack": 10, "defense": -2},
    ),
    ItemService.create_equipment(
        name="Blessed Dagger",
        description="Dagger blessed by shadow priests",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"attack": 6, "magic_power": 4},
    ),
    ItemService.create_equipment(
        name="Darkwood Bow",
        description="Bow carved from cursed wood",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"attack": 7, "max_mana": 10},
    ),
]

# ARMOR
UNCOMMON_ARMOR = [
    ItemService.create_equipment(
        name="Reinforced Chainmail",
        description="Chainmail reinforced with darksteel links",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"defense": 8, "max_health": 20},
    ),
    ItemService.create_equipment(
        name="Shadow-Touched Leather",
        description="Leather armor infused with shadow essence",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"defense": 6, "magic_power": 4},
    ),
    ItemService.create_equipment(
        name="Mystic Robes",
        description="Robes woven with void-touched threads",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"defense": 4, "max_mana": 25},
    ),
    ItemService.create_equipment(
        name="Enhanced Tower Shield",
        description="Heavy shield reinforced with dark iron",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"defense": 10, "max_health": -10},
    ),
    ItemService.create_equipment(
        name="Darksteel Plate",
        description="Armor forged from mysterious dark metal",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"defense": 12, "magic_power": -2},
    ),
]

# ACCESSORIES
UNCOMMON_ACCESSORIES = [
    ItemService.create_equipment(
        name="Darksteel Ring",
        description="Ring forged from mysterious dark metal",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"attack": 4, "magic_power": 4},
    ),
    ItemService.create_equipment(
        name="Shadow Pendant",
        description="Pendant that pulses with dark energy",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"max_health": 15, "defense": 3},
    ),
    ItemService.create_equipment(
        name="Mystic Bracers",
        description="Bracers inscribed with void runes",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"magic_power": 6, "max_mana": 15},
    ),
    ItemService.create_equipment(
        name="Enhanced Belt",
        description="Belt strengthened with darksteel buckles",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"max_health": 20, "defense": 2},
    ),
    ItemService.create_equipment(
        name="Void-Touched Amulet",
        description="Amulet that resonates with void energy",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.UNCOMMON,
        stat_modifiers={"magic_power": 8, "max_mana": 20},
    ),
]

# Combine all uncommon items
UNCOMMON_ITEMS = UNCOMMON_WEAPONS + UNCOMMON_ARMOR + UNCOMMON_ACCESSORIES

# Export for easy access
__all__ = [
    "UNCOMMON_ITEMS",
    "UNCOMMON_WEAPONS",
    "UNCOMMON_ARMOR",
    "UNCOMMON_ACCESSORIES",
]
