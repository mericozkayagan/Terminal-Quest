from .base import ItemType, ItemRarity
from ..effects.item_effects import (
    ShadowLifestealEffect,
    VoidShieldEffect,
    HopesCorruptionEffect,
    StatModifierEffect,
    OnHitEffect,
)
from ...services.item import ItemService

# Void Sentinel Set Pieces
VOID_SENTINEL_WEAPONS = [
    ItemService.create_set_piece(
        name="Blade of the Void",
        description="An ancient blade that radiates pure darkness, its edge drinking in all light",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.LEGENDARY,
        stat_modifiers={"attack": 35, "defense": 15},
        effects=[
            VoidShieldEffect(0.3),
            OnHitEffect(
                name="Void Absorption",
                description="Absorb enemy attacks into void energy",
                effect=StatModifierEffect("defense", 8),
                proc_chance=0.3,
            ),
        ],
        set_name="Void Sentinel",
    )
]

VOID_SENTINEL_ARMOR = [
    ItemService.create_set_piece(
        name="Void Sentinel's Platemail",
        description="Ancient armor that pulses with void energy, protecting its wearer from hope's taint",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.LEGENDARY,
        stat_modifiers={"defense": 40, "max_health": 80},
        effects=[VoidShieldEffect(0.35)],
        set_name="Void Sentinel",
    ),
    ItemService.create_set_piece(
        name="Void Sentinel's Helm",
        description="A helm that shields the mind from hope's whispers with pure darkness",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.LEGENDARY,
        stat_modifiers={"defense": 25, "max_health": 50},
        effects=[StatModifierEffect("resistance_to_hope", 25, is_percentage=True)],
        set_name="Void Sentinel",
    ),
]

# Hope's Bane Set Pieces
HOPES_BANE_WEAPONS = [
    ItemService.create_set_piece(
        name="Hope's End",
        description="A corrupted blade that turns hope's light against itself",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.LEGENDARY,
        stat_modifiers={"attack": 45, "magic_power": 30},
        effects=[HopesCorruptionEffect(0.4), ShadowLifestealEffect(0.2)],
        set_name="Hope's Bane",
    ),
    ItemService.create_set_piece(
        name="Staff of False Promises",
        description="A staff crackling with corrupted golden energy",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.LEGENDARY,
        stat_modifiers={"magic_power": 50, "max_mana": 60},
        effects=[
            OnHitEffect(
                name="Hope's Corruption",
                description="Corrupt enemies with false hope",
                effect=StatModifierEffect("defense", -20),
                proc_chance=0.35,
            )
        ],
        set_name="Hope's Bane",
    ),
]

HOPES_BANE_ARMOR = [
    ItemService.create_set_piece(
        name="Vestments of the Fallen Light",
        description="Robes woven from corrupted golden threads that pulse with twisted power",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.LEGENDARY,
        stat_modifiers={"defense": 30, "magic_power": 35},
        effects=[StatModifierEffect("all_damage", 15, is_percentage=True)],
        set_name="Hope's Bane",
    )
]

# Individual Legendary Items
LEGENDARY_ACCESSORIES = [
    ItemService.create_equipment(
        name="Crown of the Void Emperor",
        description="A crown of pure darkness worn by the first to resist hope's corruption",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.LEGENDARY,
        stat_modifiers={"attack": 25, "magic_power": 25, "max_health": 50},
        effects=[
            VoidShieldEffect(0.25),
            StatModifierEffect("resistance_to_hope", 20, is_percentage=True),
        ],
    ),
    ItemService.create_equipment(
        name="Heart of Corrupted Hope",
        description="A crystallized fragment of the God of Hope's power, turned against itself",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.LEGENDARY,
        stat_modifiers={"magic_power": 40, "max_mana": 80},
        effects=[
            HopesCorruptionEffect(0.3),
            StatModifierEffect("all_damage", 20, is_percentage=True),
        ],
    ),
]

# Combine all legendary items
LEGENDARY_ITEMS = (
    VOID_SENTINEL_WEAPONS
    + VOID_SENTINEL_ARMOR
    + HOPES_BANE_WEAPONS
    + HOPES_BANE_ARMOR
    + LEGENDARY_ACCESSORIES
)

# Export for easy access
__all__ = [
    "LEGENDARY_ITEMS",
    "VOID_SENTINEL_WEAPONS",
    "VOID_SENTINEL_ARMOR",
    "HOPES_BANE_WEAPONS",
    "HOPES_BANE_ARMOR",
    "LEGENDARY_ACCESSORIES",
]
