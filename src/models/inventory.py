from .items.common_consumables import HEALTH_POTION, MANA_POTION


def get_starting_items():
    """Return the starting items for a new character"""
    starting_items = []

    # Add 3 of each basic potion
    starting_items.extend([HEALTH_POTION for _ in range(3)])
    starting_items.extend([MANA_POTION for _ in range(3)])

    return starting_items
