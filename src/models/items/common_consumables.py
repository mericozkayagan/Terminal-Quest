from typing import List
from .base import ItemRarity
from ..effects.item_effects import StatModifierEffect
from ...services.item import ItemService
from .consumable import Consumable

# Create ItemService instance
item_service = ItemService()

# Basic potions for starting inventory
HEALTH_POTION = item_service.create_consumable(
    name="Health Potion",
    description="A crimson potion infused with shadow essence that restores health",
    value=20,
    rarity=ItemRarity.COMMON,
    healing=30,
    effects=[],
)

MANA_POTION = item_service.create_consumable(
    name="Mana Potion",
    description="A deep blue potion that restores magical energy",
    value=20,
    rarity=ItemRarity.COMMON,
    mana_restore=35,
    effects=[],
)

# Other common consumables
SHADOW_SALVE = item_service.create_consumable(
    name="Shadow Salve",
    description="A basic healing salve infused with shadow essence",
    value=20,
    rarity=ItemRarity.COMMON,
    healing=25,
    effects=[],
)

VOID_TINCTURE = item_service.create_consumable(
    name="Void Tincture",
    description="A simple potion that restores magical energy",
    value=25,
    rarity=ItemRarity.COMMON,
    mana_restore=30,
    effects=[],
)

DARK_BANDAGES = item_service.create_consumable(
    name="Dark Bandages",
    description="Bandages treated with shadow essence for quick healing",
    value=15,
    rarity=ItemRarity.COMMON,
    healing=15,
    effects=[StatModifierEffect("health_regen", 2, duration=3)],
)

# List of all common consumables
COMMON_CONSUMABLES = [
    HEALTH_POTION,
    MANA_POTION,
    SHADOW_SALVE,
    VOID_TINCTURE,
    DARK_BANDAGES,
]


def get_basic_consumables() -> List[Consumable]:
    """Return list of basic consumables available in shop"""
    return COMMON_CONSUMABLES


__all__ = [
    "HEALTH_POTION",
    "MANA_POTION",
    "SHADOW_SALVE",
    "VOID_TINCTURE",
    "DARK_BANDAGES",
    "COMMON_CONSUMABLES",
    "get_basic_consumables",  # Add the function to __all__
]
