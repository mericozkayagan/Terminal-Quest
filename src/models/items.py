from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random


class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    MATERIAL = "material"


class ItemRarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


@dataclass
class Item:
    name: str
    description: str
    item_type: ItemType
    value: int
    rarity: ItemRarity
    drop_chance: float = 0.1

    def use(self, target: "Character") -> bool:  # type: ignore
        """Base use method, should be overridden by specific item types"""
        return False


@dataclass
class Equipment(Item):
    stat_modifiers: Dict[str, int] = field(default_factory=dict)
    durability: int = 50
    max_durability: int = 50

    def equip(self, character: "Character"):  # type: ignore
        """Apply stat modifiers to character"""
        from .character import Character

        for stat, value in self.stat_modifiers.items():
            current = getattr(character, stat, 0)
            setattr(character, stat, current + value)

    def unequip(self, character: "Character"):  # type: ignore
        """Remove stat modifiers from character"""
        from .character import Character

        for stat, value in self.stat_modifiers.items():
            current = getattr(character, stat, 0)
            setattr(character, stat, current - value)

    def repair(self, amount: int = None):
        """Repair item durability"""
        if amount is None:
            self.durability = self.max_durability
        else:
            self.durability = min(self.max_durability, self.durability + amount)


@dataclass
class Consumable(Item):
    effects: List[Dict] = field(default_factory=list)

    def use(self, target: "Character") -> bool:  # type: ignore
        """Apply consumable effects to target"""
        from .character import Character
        from .status_effects import BLEEDING, POISONED, WEAKENED, BURNING, CURSED

        status_effect_map = {
            "BLEEDING": BLEEDING,
            "POISONED": POISONED,
            "WEAKENED": WEAKENED,
            "BURNING": BURNING,
            "CURSED": CURSED,
        }

        for effect in self.effects:
            if effect.get("heal_health"):
                target.health = min(
                    target.max_health, target.health + effect["heal_health"]
                )
            if effect.get("heal_mana"):
                target.mana = min(target.max_mana, target.mana + effect["heal_mana"])
            if effect.get("status_effect"):
                effect_name = effect["status_effect"]
                if effect_name in status_effect_map:
                    status_effect_map[effect_name].apply(target)
        return True


# Example items
RUSTY_SWORD = Equipment(
    name="Rusty Sword",
    description="An old sword with some rust spots",
    item_type=ItemType.WEAPON,
    value=20,
    rarity=ItemRarity.COMMON,
    stat_modifiers={"attack": 3},
    durability=50,
    max_durability=50,
    drop_chance=0.15,
)

LEATHER_ARMOR = Equipment(
    name="Leather Armor",
    description="Basic protection made of leather",
    item_type=ItemType.ARMOR,
    value=25,
    rarity=ItemRarity.COMMON,
    stat_modifiers={"defense": 2, "max_health": 10},
    durability=40,
    max_durability=40,
    drop_chance=0.12,
)

HEALING_SALVE = Consumable(
    name="Healing Salve",
    description="A medicinal salve that heals wounds",
    item_type=ItemType.CONSUMABLE,
    value=15,
    rarity=ItemRarity.COMMON,
    effects=[{"heal_health": 30}],
    drop_chance=0.2,
)

POISON_VIAL = Consumable(
    name="Poison Vial",
    description="A vial of toxic substance",
    item_type=ItemType.CONSUMABLE,
    value=20,
    rarity=ItemRarity.UNCOMMON,
    effects=[{"status_effect": "POISONED"}],
    drop_chance=0.1,
)

# More powerful items
VAMPIRIC_BLADE = Equipment(
    name="Vampiric Blade",
    description="A cursed blade that drains life force",
    item_type=ItemType.WEAPON,
    value=75,
    rarity=ItemRarity.RARE,
    stat_modifiers={"attack": 8, "max_health": 15},
    durability=60,
    max_durability=60,
    drop_chance=0.05,
)

CURSED_AMULET = Equipment(
    name="Cursed Amulet",
    description="An amulet pulsing with dark energy",
    item_type=ItemType.ACCESSORY,
    value=100,
    rarity=ItemRarity.EPIC,
    stat_modifiers={"attack": 5, "max_mana": 25, "defense": -2},
    durability=40,
    max_durability=40,
    drop_chance=0.03,
)


def generate_random_item() -> Equipment:
    """Generate a random item with appropriate stats"""
    rarity = random.choices(list(ItemRarity), weights=[50, 30, 15, 4, 1], k=1)[0]

    # Base value multipliers by rarity
    value_multipliers = {
        ItemRarity.COMMON: 1,
        ItemRarity.UNCOMMON: 2,
        ItemRarity.RARE: 4,
        ItemRarity.EPIC: 8,
        ItemRarity.LEGENDARY: 16,
    }

    # Item prefixes by rarity
    prefixes = {
        ItemRarity.COMMON: ["Iron", "Steel", "Leather", "Wooden"],
        ItemRarity.UNCOMMON: ["Reinforced", "Enhanced", "Blessed", "Mystic"],
        ItemRarity.RARE: ["Shadowforged", "Soulbound", "Cursed", "Ethereal"],
        ItemRarity.EPIC: ["Demonforged", "Nightweaver's", "Bloodbound", "Voidtouched"],
        ItemRarity.LEGENDARY: ["Ancient", "Dragon", "Godslayer's", "Apocalyptic"],
    }

    # Item types and their base stats
    item_types = {
        ItemType.WEAPON: [("Sword", {"attack": 5}), ("Dagger", {"attack": 3})],
        ItemType.ARMOR: [
            ("Armor", {"defense": 3, "max_health": 10}),
            ("Shield", {"defense": 5}),
        ],
        ItemType.ACCESSORY: [
            ("Amulet", {"max_mana": 10, "max_health": 5}),
            ("Ring", {"attack": 2, "max_mana": 5}),
        ],
    }

    # Choose item type and specific item
    item_type = random.choice(list(item_types.keys()))
    item_name, base_stats = random.choice(item_types[item_type])

    # Generate name and description
    prefix = random.choice(prefixes[rarity])
    name = f"{prefix} {item_name}"
    description = (
        f"A {rarity.value.lower()} {item_name.lower()} imbued with dark energy"
    )

    # Calculate value
    base_value = 50
    value = base_value * value_multipliers[rarity]

    # Scale stats based on rarity
    stat_modifiers = {
        stat: value * value_multipliers[rarity] for stat, value in base_stats.items()
    }

    return Equipment(
        name=name,
        description=description,
        item_type=item_type,
        value=value,
        rarity=rarity,
        stat_modifiers=stat_modifiers,
        durability=100,
        max_durability=100,
        drop_chance=0.1,
    )
