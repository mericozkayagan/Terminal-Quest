import random
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING, Callable

from ..models.items.base import ItemRarity, Item
from ..models.items.consumable import Consumable
from ..models.base_types import ItemType, GameEntity
from ..models.effects.base import BaseEffect

if TYPE_CHECKING:
    from ..models.character import Character, Enemy
    from ..models.items.equipment import Equipment
    from ..models.items.consumable import Consumable

DROP_SETTINGS = {
    "BASE_DROP_CHANCE": 0.3,
    "LEVEL_SCALING": {"DROP_CHANCE": 0.01, "RARITY_BOOST": 0.02},
    "BOSS_SETTINGS": {
        "GUARANTEED_DROPS": 2,
        "RARITY_BOOST": 0.2,
        "SET_PIECE_CHANCE": 0.3,
    },
    "RARITY_THRESHOLDS": {
        ItemRarity.LEGENDARY: 0.95,
        ItemRarity.EPIC: 0.85,
        ItemRarity.RARE: 0.70,
        ItemRarity.UNCOMMON: 0.40,
        ItemRarity.COMMON: 0.0,
    },
}


class ItemService:
    """Handles item creation and management"""

    @staticmethod
    def create_consumable(
        name: str,
        description: str,
        rarity: ItemRarity = ItemRarity.COMMON,
        healing: Optional[int] = None,
        mana_restore: Optional[int] = None,
        effects: Optional[List[BaseEffect]] = None,
        use_effect: Optional[Callable[[GameEntity], bool]] = None,
        value: int = 0,
    ) -> "Consumable":
        """
        Create a consumable item with optional healing, mana restoration, or custom effects

        Args:
            name: Item name
            description: Item description
            rarity: Item rarity (default: COMMON)
            healing: Amount of health to restore (optional)
            mana_restore: Amount of mana to restore (optional)
            effects: List of additional effects (optional)
            use_effect: Custom use effect (optional)
            value: Item value in gold (default: 0)
        """
        if healing is not None:

            def healing_effect(character: "Character") -> bool:
                if character.health < character.max_health:
                    character.health = min(
                        character.health + healing, character.max_health
                    )
                    if effects:
                        for effect in effects:
                            effect.apply(character)
                    return True
                return False

            use_effect = healing_effect

        elif mana_restore is not None:

            def mana_effect(character: "Character") -> bool:
                if character.mana < character.max_mana:
                    character.mana = min(
                        character.mana + mana_restore, character.max_mana
                    )
                    if effects:
                        for effect in effects:
                            effect.apply(character)
                    return True
                return False

            use_effect = mana_effect

        return Consumable(
            name=name,
            description=description,
            rarity=rarity,
            use_effect=use_effect,
            value=value,
            effects=effects,
        )

    @staticmethod
    def create_set_piece(
        name: str,
        description: str,
        item_type: ItemType,
        rarity: ItemRarity,
        stat_modifiers: dict,
        effects: List["BaseEffect"],
        set_name: str,
    ) -> "Equipment":
        from ..models.items.equipment import Equipment

        return Equipment(
            name=name,
            description=description,
            item_type=item_type,
            rarity=rarity,
            value=ItemService.calculate_value(rarity),
            stat_modifiers=stat_modifiers,
            effects=effects,
            set_name=set_name,
        )

    @staticmethod
    def calculate_value(rarity: ItemRarity) -> int:
        """Calculate base value based on item rarity"""
        base_values = {
            ItemRarity.COMMON: 15,
            ItemRarity.UNCOMMON: 30,
            ItemRarity.RARE: 75,
            ItemRarity.EPIC: 150,
            ItemRarity.LEGENDARY: 300,
        }
        return base_values[rarity]

    @staticmethod
    def generate_random_item(
        rarity: Optional[ItemRarity] = None, item_type: Optional[ItemType] = None
    ) -> Item:
        """Generate a random item with optional rarity/type constraints"""
        if not rarity:
            rarity = ItemService._random_rarity()
        if not item_type:
            item_type = random.choice(list(ItemType))

        # Generate appropriate stats for the item type
        base_stats = ItemService._generate_base_stats(item_type)

        return ItemService.create_equipment(
            name=f"{rarity.value} {item_type.value.title()}",
            description=f"A {rarity.value.lower()} {item_type.value}",
            item_type=item_type,
            rarity=rarity,
            stat_modifiers=base_stats,
        )

    @staticmethod
    def _calculate_value(rarity: ItemRarity, stats: Dict[str, int]) -> int:
        """Calculate item value based on rarity and stats"""
        base_value = sum(abs(value) for value in stats.values()) * 10
        rarity_multipliers = {
            ItemRarity.COMMON: 1,
            ItemRarity.UNCOMMON: 2,
            ItemRarity.RARE: 4,
            ItemRarity.EPIC: 8,
            ItemRarity.LEGENDARY: 16,
        }
        return base_value * rarity_multipliers[rarity]

    @staticmethod
    def _random_rarity() -> ItemRarity:
        """Generate random rarity based on drop chances"""
        roll = random.random()
        if roll < 0.01:
            return ItemRarity.LEGENDARY
        elif roll < 0.04:
            return ItemRarity.EPIC
        elif roll < 0.09:
            return ItemRarity.RARE
        elif roll < 0.19:
            return ItemRarity.UNCOMMON
        return ItemRarity.COMMON

    @staticmethod
    def get_enemy_drops(enemy: "Enemy") -> List[Item]:
        """Generate drops for an enemy, returns a list of items"""
        drops = []

        # Base drop chance scaled with enemy level
        drop_chance = DROP_SETTINGS["BASE_DROP_CHANCE"] + (
            enemy.level * DROP_SETTINGS["LEVEL_SCALING"]["DROP_CHANCE"]
        )

        # Higher level enemies have better drops
        rarity_boost = enemy.level * DROP_SETTINGS["LEVEL_SCALING"]["RARITY_BOOST"]

        # Boss enemies have guaranteed drops
        if getattr(enemy, "is_boss", False):
            for _ in range(DROP_SETTINGS["BOSS_SETTINGS"]["GUARANTEED_DROPS"]):
                rarity = ItemService._get_rarity_with_boost(
                    rarity_boost + DROP_SETTINGS["BOSS_SETTINGS"]["RARITY_BOOST"]
                )
                item = ItemService.generate_random_item(rarity)
                drops.append(item)

            # Chance for set piece on boss kills
            if random.random() < DROP_SETTINGS["BOSS_SETTINGS"]["SET_PIECE_CHANCE"]:
                set_piece = ItemService.generate_random_set_piece(
                    ItemService._get_rarity_with_boost(rarity_boost * 1.5)
                )
                if set_piece:
                    drops.append(set_piece)

        # Regular drop chance
        elif random.random() < drop_chance:
            rarity = ItemService._get_rarity_with_boost(rarity_boost)
            item = ItemService.generate_random_item(rarity)
            drops.append(item)

        return drops

    @staticmethod
    def _get_rarity_with_boost(rarity_boost: float = 0.0) -> ItemRarity:
        """Get rarity with level-based boost"""
        roll = random.random() + rarity_boost

        for rarity, threshold in DROP_SETTINGS["RARITY_THRESHOLDS"].items():
            if roll >= threshold:
                return rarity

        return ItemRarity.COMMON

    @staticmethod
    def _generate_base_stats(item_type: ItemType) -> Dict[str, int]:
        """Generate appropriate base stats for an item type"""
        if item_type == ItemType.WEAPON:
            return {"attack": random.randint(3, 8)}
        elif item_type == ItemType.ARMOR:
            return {
                "defense": random.randint(2, 6),
                "max_health": random.randint(5, 15),
            }
        elif item_type == ItemType.ACCESSORY:
            stat_choices = [
                "attack",
                "defense",
                "magic_power",
                "max_health",
                "max_mana",
            ]
            stat = random.choice(stat_choices)
            return {stat: random.randint(2, 5)}
        return {}

    @staticmethod
    def create_equipment(
        name: str,
        description: str,
        item_type: ItemType,
        rarity: ItemRarity,
        stat_modifiers: Dict[str, int],
        effects: List[BaseEffect] = None,
    ) -> "Equipment":
        """Create equipment with given parameters"""
        from ..models.items.equipment import Equipment

        return Equipment(
            name=name,
            description=description,
            item_type=item_type,
            rarity=rarity,
            value=ItemService.calculate_value(rarity),
            stat_modifiers=stat_modifiers,
            effects=effects or [],
        )

    @staticmethod
    def generate_random_set_piece(rarity: ItemRarity) -> Optional["Equipment"]:
        """Generate a set piece from existing sets with given rarity"""
        from ..models.items.sets import ITEM_SETS

        # Filter sets by rarity
        available_sets = [s for s in ITEM_SETS if s.rarity == rarity]
        if not available_sets:
            return None

        # Choose a random set
        chosen_set = random.choice(available_sets)

        # Get first bonus stats as base stats for the piece
        base_stats = chosen_set.bonuses[0].stat_bonuses

        return ItemService.create_set_piece(
            name=f"{chosen_set.name} Piece",
            description=chosen_set.description,
            item_type=ItemType.ARMOR,  # Set pieces are typically armor
            rarity=rarity,
            stat_modifiers=base_stats,
            effects=chosen_set.bonuses[0].effects,
            set_name=chosen_set.name,
        )

    def get_all_items(self) -> List[Item]:
        """Get all predefined items"""
        from src.models.items.common_items import COMMON_ITEMS
        from src.models.items.uncommon_items import UNCOMMON_ITEMS
        from src.models.items.rare_items import RARE_ITEMS
        from src.models.items.epic_items import EPIC_ITEMS
        from src.models.items.legendary_items import LEGENDARY_ITEMS

        all_items = []
        all_items.extend(COMMON_ITEMS)
        all_items.extend(UNCOMMON_ITEMS)
        all_items.extend(RARE_ITEMS)
        all_items.extend(EPIC_ITEMS)
        all_items.extend(LEGENDARY_ITEMS)
        return all_items
