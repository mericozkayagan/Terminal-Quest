from typing import Dict, Any, Optional
from src.models.base_types import ItemType, ItemRarity


class Item:
    """Base class for all items in the game"""

    def __init__(
        self,
        name: str,
        description: str = "",
        value: int = 0,
        rarity: Optional[ItemRarity] = ItemRarity.COMMON,
    ):
        self.name = name
        self.description = description
        self.value = value
        self.rarity = rarity

    def get_info(self) -> Dict[str, Any]:
        """Get basic item information"""
        return {
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "rarity": self.rarity.name if self.rarity else "COMMON",
        }

    def __str__(self) -> str:
        return f"{self.name} ({self.rarity.name if self.rarity else 'COMMON'})"
