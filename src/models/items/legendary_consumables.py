from dataclasses import __all__
from models.items.legendary_items import LEGENDARY_ITEMS
from .base import ItemRarity
from ..effects.item_effects import (
    ShadowLifestealEffect,
    VoidShieldEffect,
    StatModifierEffect,
    HopesCorruptionEffect,
)
from ...services.item import ItemService

LEGENDARY_CONSUMABLES = [
    ItemService.create_consumable(
        name="Crystallized Void",
        description="A shard of pure darkness crystallized into consumable form",
        value=300,
        rarity=ItemRarity.LEGENDARY,
        healing=100,
        mana_restore=100,
        effects=[
            VoidShieldEffect(0.5),
            StatModifierEffect("all_damage", 25, is_percentage=True, duration=3),
            StatModifierEffect(
                "resistance_to_hope", 40, is_percentage=True, duration=3
            ),
        ],
    ),
    ItemService.create_consumable(
        name="Essence of the Void Sentinel",
        description="Concentrated power of those who guard against hope's corruption",
        value=350,
        rarity=ItemRarity.LEGENDARY,
        healing=150,
        effects=[
            VoidShieldEffect(0.4),
            StatModifierEffect("defense", 30, duration=5),
            StatModifierEffect("max_health", 100, duration=5),
        ],
    ),
    ItemService.create_consumable(
        name="Hope's Corruption",
        description="A vial of corrupted golden light, turned against itself",
        value=400,
        rarity=ItemRarity.LEGENDARY,
        mana_restore=200,
        effects=[
            HopesCorruptionEffect(0.5),
            StatModifierEffect("magic_power", 40, duration=3),
            StatModifierEffect("all_damage", 30, is_percentage=True, duration=3),
        ],
    ),
    ItemService.create_consumable(
        name="Tears of the Hopeless",
        description="Crystallized despair that grants immense power at a terrible cost",
        value=500,
        rarity=ItemRarity.LEGENDARY,
        effects=[
            StatModifierEffect("all_damage", 50, is_percentage=True, duration=3),
            StatModifierEffect("max_health", -50, duration=3),
            ShadowLifestealEffect(0.3),
        ],
    ),
]

# Add to legendary items
LEGENDARY_ITEMS.extend(LEGENDARY_CONSUMABLES)

# Update exports
__all__.append("LEGENDARY_CONSUMABLES")
