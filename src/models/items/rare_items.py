from .base import ItemType, ItemRarity
from ..effects.item_effects import (
    OnHitEffect,
    StatModifierEffect,
    ShadowLifestealEffect,
    VoidShieldEffect,
    HopeBaneEffect,
)
from ...services.item import ItemService

# WEAPONS
RARE_WEAPONS = [
    ItemService.create_equipment(
        name="Hope's Bane",
        description="A blade that drinks the golden light of corrupted hope",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.RARE,
        stat_modifiers={"attack": 15, "magic_power": -5},
        effects=[HopeBaneEffect()],
    ),
    ItemService.create_equipment(
        name="Shadowforged Claymore",
        description="A massive sword that radiates pure darkness, shielding its wielder from hope's taint",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.RARE,
        stat_modifiers={"attack": 12, "defense": 8},
        effects=[VoidShieldEffect(0.15)],
    ),
    ItemService.create_equipment(
        name="Void Whisperer",
        description="A staff carved from crystallized darkness, it hungers for the light of hope",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.RARE,
        stat_modifiers={"magic_power": 18, "max_mana": 25},
        effects=[
            OnHitEffect(
                name="Hope Drinker",
                description="Drains enemy's golden corruption",
                effect=StatModifierEffect("magic_power", 8),
                proc_chance=0.25,
            )
        ],
    ),
]

# ARMOR
RARE_ARMOR = [
    ItemService.create_equipment(
        name="Dark Sentinel's Plate",
        description="Armor forged for those who guard against hope's invasion",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.RARE,
        stat_modifiers={"defense": 15, "max_health": 30},
        effects=[
            OnHitEffect(
                name="Shadow Ward",
                description="Converts hope's corruption into protective shadows",
                effect=StatModifierEffect("defense", 12),
                proc_chance=0.2,
            )
        ],
    ),
    ItemService.create_equipment(
        name="Void-Touched Robes",
        description="Robes woven from pure darkness, they absorb the golden light of corruption",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.RARE,
        stat_modifiers={"defense": 8, "max_mana": 45},
        effects=[VoidShieldEffect(0.2)],
    ),
]

# ACCESSORIES
RARE_ACCESSORIES = [
    ItemService.create_equipment(
        name="Sigil of the Shadow Sworn",
        description="A dark sigil worn by those who've sworn to fight the God of Hope",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.RARE,
        stat_modifiers={"attack": 10, "magic_power": 10},
        effects=[StatModifierEffect("resistance_to_hope", 15, is_percentage=True)],
    ),
    ItemService.create_equipment(
        name="Pendant of Dark Comfort",
        description="This pendant reminds the wearer that in darkness lies salvation",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.RARE,
        stat_modifiers={"max_health": 25, "defense": 8},
        effects=[ShadowLifestealEffect(0.12)],
    ),
    ItemService.create_equipment(
        name="Ring of the Void Guardian",
        description="Worn by those who understand that hope brings only madness",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.RARE,
        stat_modifiers={"magic_power": 12, "max_mana": 30},
        effects=[
            OnHitEffect(
                name="Hope's Bane",
                description="Attacks weaken the corruption of hope",
                effect=StatModifierEffect("magic_power", -5),
                proc_chance=0.3,
            )
        ],
    ),
]

# CONSUMABLES
RARE_CONSUMABLES = [
    ItemService.create_consumable(
        name="Essence of Shadow",
        description="Distilled darkness that cleanses hope's corruption",
        value=120,
        rarity=ItemRarity.RARE,
        healing=50,
        effects=[
            StatModifierEffect("resistance_to_hope", 25, is_percentage=True, duration=3)
        ],
    ),
    ItemService.create_consumable(
        name="Void Elixir",
        description="A potion that temporarily grants the protection of pure darkness",
        value=150,
        rarity=ItemRarity.RARE,
        mana_restore=60,
        effects=[VoidShieldEffect(0.3)],
    ),
]

# Combine all rare items
RARE_ITEMS = RARE_WEAPONS + RARE_ARMOR + RARE_ACCESSORIES + RARE_CONSUMABLES

# Export for easy access
__all__ = [
    "RARE_ITEMS",
    "RARE_WEAPONS",
    "RARE_ARMOR",
    "RARE_ACCESSORIES",
    "RARE_CONSUMABLES",
]
