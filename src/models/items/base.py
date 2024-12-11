from enum import Enum
from uuid import uuid4
from ..base_types import ItemType, ItemRarity


class Item:
    def __init__(
        self,
        name: str,
        description: str,
        item_type: ItemType,
        rarity: ItemRarity,
        value: int,
    ):
        self.name = name
        self.description = description
        self.item_type = item_type
        self.rarity = rarity
        self.value = value
        self.id = str(uuid4())

    @property
    def drop_chance(self) -> float:
        return self.rarity.drop_chance

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return (
            self.name == other.name
            and self.description == other.description
            and self.item_type == other.item_type
            and self.rarity == other.rarity
        )

    def __hash__(self):
        return hash((self.name, self.description, self.item_type, self.rarity))
