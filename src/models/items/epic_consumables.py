from .base import ItemRarity
from ..effects.item_effects import (
    ShadowLifestealEffect,
    VoidShieldEffect,
    StatModifierEffect,
)
from ...services.item import ItemService

# Epic Consumables
EPIC_CONSUMABLES = [
    ItemService.create_consumable(
        name="Shadow King's Elixir",
        description="A powerful concoction that grants the strength of ancient shadow rulers",
        value=200,
        rarity=ItemRarity.EPIC,
        healing=75,
        mana_restore=75,
        effects=[
            StatModifierEffect("all_damage", 20, is_percentage=True, duration=3),
            ShadowLifestealEffect(0.15),
        ],
    ),
    ItemService.create_consumable(
        name="Void Walker's Essence",
        description="Essence that allows temporary mastery over the void",
        value=250,
        rarity=ItemRarity.EPIC,
        effects=[
            VoidShieldEffect(0.35),
            StatModifierEffect("magic_power", 25, duration=3),
            StatModifierEffect("max_mana", 50, duration=3),
        ],
    ),
]

__all__ = ["EPIC_CONSUMABLES"]
