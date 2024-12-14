from .base import ItemType, ItemRarity
from ..effects.item_effects import (
    ShadowLifestealEffect,
    VoidShieldEffect,
    VoidBoltEffect,
    HopesCorruptionEffect,
)
from ...services.item import ItemService

# Shadow Assassin Set Pieces
SHADOW_ASSASSIN_WEAPONS = [
    ItemService.create_set_piece(
        name="Blade",
        description="A blade that drinks light itself, leaving only void in its wake",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"attack": 25, "magic_power": 15},
        effects=[ShadowLifestealEffect(0.15)],
        set_name="Shadow Assassin",
    ),
    ItemService.create_set_piece(
        name="Offhand Dagger",
        description="A dagger that cuts through hope's radiance",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"attack": 18, "magic_power": 12},
        effects=[HopesCorruptionEffect(0.25)],
        set_name="Shadow Assassin",
    ),
]

SHADOW_ASSASSIN_ARMOR = [
    ItemService.create_set_piece(
        name="Shadowcloak",
        description="A cloak woven from pure darkness that devours hope's light",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"defense": 20, "max_health": 40},
        effects=[VoidShieldEffect(0.2)],
        set_name="Shadow Assassin",
    )
]

# Darkweaver Set Pieces
DARKWEAVER_WEAPONS = [
    ItemService.create_set_piece(
        name="Void Staff",
        description="A staff that channels the power of absolute darkness",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"magic_power": 30, "max_mana": 50},
        effects=[VoidBoltEffect(0.25)],
        set_name="Darkweaver",
    )
]

DARKWEAVER_ARMOR = [
    ItemService.create_set_piece(
        name="Dark Robes",
        description="Robes that absorb hope's corruption, turning it to power",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"defense": 15, "max_mana": 60},
        effects=[VoidShieldEffect(0.15)],
        set_name="Darkweaver",
    ),
    ItemService.create_set_piece(
        name="Shadow Cowl",
        description="A hood that shields the mind from hope's whispers",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"defense": 12, "magic_power": 20},
        effects=[VoidBoltEffect(0.2)],
        set_name="Darkweaver",
    ),
]

# Individual Epic Items
EPIC_WEAPONS = [
    ItemService.create_equipment(
        name="Twilight's Edge",
        description="A sword forged at the boundary between light and shadow",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"attack": 28, "magic_power": 18},
        effects=[ShadowLifestealEffect(0.18), HopesCorruptionEffect(0.2)],
    ),
    ItemService.create_equipment(
        name="Void Siphon",
        description="A staff that draws power from the absence of hope",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"magic_power": 35, "max_mana": 45},
        effects=[VoidBoltEffect(0.3)],
    ),
]

EPIC_ARMOR = [
    ItemService.create_equipment(
        name="Mantle of the Hopeless",
        description="A cloak that turns despair into protective shadows",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"defense": 25, "max_health": 50},
        effects=[VoidShieldEffect(0.25)],
    )
]

EPIC_ACCESSORIES = [
    ItemService.create_equipment(
        name="Crown of Dark Resolve",
        description="A crown that strengthens as hope fades",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"magic_power": 25, "max_mana": 40},
        effects=[VoidBoltEffect(0.2)],
    ),
    ItemService.create_equipment(
        name="Void Heart Amulet",
        description="An amulet containing a shard of pure darkness",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.EPIC,
        stat_modifiers={"attack": 20, "magic_power": 20},
        effects=[ShadowLifestealEffect(0.12)],
    ),
]

# Combine all epic items
EPIC_ITEMS = (
    SHADOW_ASSASSIN_WEAPONS
    + SHADOW_ASSASSIN_ARMOR
    + DARKWEAVER_WEAPONS
    + DARKWEAVER_ARMOR
    + EPIC_WEAPONS
    + EPIC_ARMOR
    + EPIC_ACCESSORIES
)

# Export for easy access
__all__ = [
    "EPIC_ITEMS",
    "SHADOW_ASSASSIN_WEAPONS",
    "SHADOW_ASSASSIN_ARMOR",
    "DARKWEAVER_WEAPONS",
    "DARKWEAVER_ARMOR",
    "EPIC_WEAPONS",
    "EPIC_ARMOR",
    "EPIC_ACCESSORIES",
]
