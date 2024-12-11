from typing import Dict, List, Optional

from .base import ItemType, Item, ItemRarity
from ..effects.base import BaseEffect


class Equipment(Item):
    def __init__(
        self,
        name: str,
        description: str,
        item_type: ItemType,
        rarity: ItemRarity,
        value: int,
        stat_modifiers: Optional[Dict[str, int]] = None,
        effects: Optional[List["BaseEffect"]] = None,
        set_name: Optional[str] = None,
    ):
        super().__init__(name, description, item_type, rarity, value)
        self.stat_modifiers = stat_modifiers or {}
        self.effects = effects or []
        self.set_name = set_name
        self.max_durability = {
            ItemRarity.COMMON: 40,
            ItemRarity.UNCOMMON: 50,
            ItemRarity.RARE: 60,
            ItemRarity.EPIC: 80,
            ItemRarity.LEGENDARY: 100,
        }[self.rarity]
        self.durability = self.max_durability
