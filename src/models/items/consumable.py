from typing import Optional, Callable, List, TYPE_CHECKING
from .base import Item
from ..base_types import ItemType, ItemRarity
from ..effects.base import BaseEffect

if TYPE_CHECKING:
    from ..character import Character


class Consumable(Item):
    def __init__(
        self,
        name: str,
        description: str,
        rarity: ItemRarity = ItemRarity.COMMON,
        use_effect: Optional[Callable[["Character"], bool]] = None,
        value: int = 0,
        effects: Optional[List[BaseEffect]] = None,
    ):
        super().__init__(
            name=name,
            description=description,
            item_type=ItemType.CONSUMABLE,
            rarity=rarity,
            value=value,
        )
        self.use_effect = use_effect
        self.effects = effects or []

    def use(self, user: "Character") -> bool:
        if self.use_effect:
            success = self.use_effect(user)
            if success and self.effects:
                for effect in self.effects:
                    effect.apply(user)
            return success
        return False
