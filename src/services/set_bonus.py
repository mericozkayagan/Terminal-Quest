from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.character import Character
    from ..models.sets.base import SetBonus


class SetBonusService:
    @staticmethod
    def check_set_bonuses(character: "Character") -> Dict[str, List["SetBonus"]]:
        """Check and return active set bonuses for a character"""
        from ..models.sets.base import ITEM_SETS

        active_sets: Dict[str, List["SetBonus"]] = {}
        equipped_set_pieces: Dict[str, int] = {}

        # Count equipped set pieces
        for item in character.equipment.values():
            if item and item.set_name:
                equipped_set_pieces[item.set_name] = (
                    equipped_set_pieces.get(item.set_name, 0) + 1
                )

        # Check which set bonuses are active
        for set_name, count in equipped_set_pieces.items():
            if set_name in ITEM_SETS:
                set_item = ITEM_SETS[set_name]
                active_bonuses = set_item.get_active_bonuses(count)
                if active_bonuses:
                    active_sets[set_name] = active_bonuses

        return active_sets
