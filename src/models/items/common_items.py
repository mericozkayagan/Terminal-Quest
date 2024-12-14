from .base import ItemType, ItemRarity
from ...services.item import ItemService

# WEAPONS
COMMON_WEAPONS = [
    ItemService.create_equipment(
        name="Iron Sword",
        description="Standard military-issue sword, dulled by darkness",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 5},
    ),
    ItemService.create_equipment(
        name="Wooden Bow",
        description="Bow carved from darkwood trees",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 4, "speed": 1},
    ),
    ItemService.create_equipment(
        name="Steel Dagger",
        description="Quick blade for swift strikes from shadow",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 3, "speed": 2},
    ),
    ItemService.create_equipment(
        name="Training Staff",
        description="Simple staff used by apprentice shadowcasters",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 2, "magic_power": 3},
    ),
    ItemService.create_equipment(
        name="Militia Spear",
        description="Standard-issue spear for the town guard",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 4, "defense": 1},
    ),
    ItemService.create_equipment(
        name="Hunter's Crossbow",
        description="Reliable crossbow for hunting in darkness",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 6, "speed": -1},
    ),
    ItemService.create_equipment(
        name="Blacksmith Hammer",
        description="Heavy hammer that doubles as a weapon",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 5, "defense": 1},
    ),
    ItemService.create_equipment(
        name="Throwing Knives",
        description="Set of balanced knives for throwing",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 2, "speed": 3},
    ),
    ItemService.create_equipment(
        name="Iron Mace",
        description="Simple but effective bludgeoning weapon",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 6},
    ),
    ItemService.create_equipment(
        name="Apprentice Wand",
        description="Basic wand for channeling dark magic",
        item_type=ItemType.WEAPON,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"magic_power": 4, "max_mana": 5},
    ),
]

# ARMOR
COMMON_ARMOR = [
    ItemService.create_equipment(
        name="Leather Armor",
        description="Basic protection crafted from treated leather",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 3, "max_health": 10},
    ),
    ItemService.create_equipment(
        name="Iron Chainmail",
        description="Linked rings of iron providing decent protection",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 4, "max_health": 5},
    ),
    ItemService.create_equipment(
        name="Padded Armor",
        description="Quilted armor offering basic protection",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 2, "max_health": 15},
    ),
    ItemService.create_equipment(
        name="Scout's Leather",
        description="Light armor favored by scouts",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 2, "speed": 2},
    ),
    ItemService.create_equipment(
        name="Iron Breastplate",
        description="Basic chest protection",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 5},
    ),
    ItemService.create_equipment(
        name="Wooden Shield",
        description="Simple shield reinforced with iron bands",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 4, "max_health": 5},
    ),
    ItemService.create_equipment(
        name="Iron Shield",
        description="Standard-issue iron shield",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 5},
    ),
    ItemService.create_equipment(
        name="Cloth Robes",
        description="Simple robes worn by apprentice mages",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 1, "max_mana": 10},
    ),
    ItemService.create_equipment(
        name="Leather Boots",
        description="Standard footwear for travelers",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 1, "speed": 2},
    ),
    ItemService.create_equipment(
        name="Iron Gauntlets",
        description="Basic hand protection",
        item_type=ItemType.ARMOR,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 2, "attack": 1},
    ),
]

# ACCESSORIES
COMMON_ACCESSORIES = [
    ItemService.create_equipment(
        name="Iron Ring",
        description="Plain ring that focuses minor energy",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"max_mana": 5},
    ),
    ItemService.create_equipment(
        name="Leather Belt",
        description="Sturdy belt with pouches",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"max_health": 5, "defense": 1},
    ),
    ItemService.create_equipment(
        name="Training Amulet",
        description="Basic amulet for apprentice mages",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"magic_power": 2, "max_mana": 5},
    ),
    ItemService.create_equipment(
        name="Iron Bracers",
        description="Simple arm protection",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 2},
    ),
    ItemService.create_equipment(
        name="Cloth Sash",
        description="Light sash with minor enchantments",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"speed": 2},
    ),
    ItemService.create_equipment(
        name="Traveler's Pendant",
        description="Common pendant worn by travelers",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"max_health": 8},
    ),
    ItemService.create_equipment(
        name="Iron Pendant",
        description="Simple iron pendant",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"defense": 1, "max_health": 5},
    ),
    ItemService.create_equipment(
        name="Leather Gloves",
        description="Basic protective gloves",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 1, "defense": 1},
    ),
    ItemService.create_equipment(
        name="Cloth Headband",
        description="Simple cloth headband",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"max_mana": 8},
    ),
    ItemService.create_equipment(
        name="Training Ring",
        description="Ring used by combat trainees",
        item_type=ItemType.ACCESSORY,
        rarity=ItemRarity.COMMON,
        stat_modifiers={"attack": 2},
    ),
]

# Combine all common items into one list
COMMON_ITEMS = COMMON_WEAPONS + COMMON_ARMOR + COMMON_ACCESSORIES

# Export for easy access
__all__ = ["COMMON_ITEMS", "COMMON_WEAPONS", "COMMON_ARMOR", "COMMON_ACCESSORIES"]
