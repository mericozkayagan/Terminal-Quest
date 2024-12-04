from typing import Dict, Tuple

# Game version
VERSION = "1.0.0"

# Game balance settings
GAME_BALANCE = {
    # Level up settings
    "BASE_EXP_TO_LEVEL": 100,
    "LEVEL_UP_EXP_MULTIPLIER": 1.5,
    "LEVEL_UP_HEALTH_INCREASE": 20,
    "LEVEL_UP_MANA_INCREASE": 15,
    "LEVEL_UP_ATTACK_INCREASE": 5,
    "LEVEL_UP_DEFENSE_INCREASE": 3,

    # Combat settings
    "RUN_CHANCE": 0.4,
    "DAMAGE_RANDOMNESS_RANGE": (-3, 3),

    # Shop settings
    "SELL_PRICE_MULTIPLIER": 0.5,  # Items sell for half their buy price
}

# Character stat ranges
STAT_RANGES: Dict[str, Tuple[int, int]] = {
    # Character class stat ranges
    "CLASS_HEALTH": (85, 120),
    "CLASS_ATTACK": (12, 18),
    "CLASS_DEFENSE": (3, 8),
    "CLASS_MANA": (60, 100),

    # Enemy stat ranges
    "ENEMY_HEALTH": (30, 100),
    "ENEMY_ATTACK": (8, 25),
    "ENEMY_DEFENSE": (2, 10),
    "ENEMY_EXP": (20, 100),
    "ENEMY_GOLD": (10, 100),

    # Skill stat ranges
    "SKILL_DAMAGE": (15, 30),
    "SKILL_MANA_COST": (10, 25)
}

# Starting inventory
STARTING_INVENTORY = {
    "Health Potion": 2,
    "Mana Potion": 2,
    "Gold": 0,
    "items": []
}

# Item settings
ITEM_SETTINGS = {
    # Durability ranges
    "COMMON_DURABILITY": (40, 60),
    "RARE_DURABILITY": (60, 80),
    "EPIC_DURABILITY": (80, 100),

    # Drop chances by rarity
    "DROP_CHANCES": {
        "COMMON": 0.15,
        "UNCOMMON": 0.10,
        "RARE": 0.05,
        "EPIC": 0.03,
        "LEGENDARY": 0.01
    }
}

# Status effect settings
STATUS_EFFECT_SETTINGS = {
    "BLEEDING": {
        "DURATION": 3,
        "DAMAGE": 5,
        "CHANCE": 0.7
    },
    "POISONED": {
        "DURATION": 4,
        "DAMAGE": 3,
        "ATTACK_REDUCTION": 2,
        "CHANCE": 0.6
    },
    "WEAKENED": {
        "DURATION": 2,
        "ATTACK_REDUCTION": 3,
        "DEFENSE_REDUCTION": 2,
        "CHANCE": 0.8
    },
    "BURNING": {
        "DURATION": 2,
        "DAMAGE": 7,
        "CHANCE": 0.65
    },
    "CURSED": {
        "DURATION": 3,
        "DAMAGE": 2,
        "ATTACK_REDUCTION": 2,
        "DEFENSE_REDUCTION": 1,
        "MANA_REDUCTION": 10,
        "CHANCE": 0.5
    }
}

# Display settings
DISPLAY_SETTINGS = {
    "TYPE_SPEED": 0.03,
    "COMBAT_MESSAGE_DELAY": 1.0,
    "LEVEL_UP_DELAY": 2.0
}

# AI Generation settings
AI_SETTINGS = {
    "MAX_RETRIES": 3,
    "TEMPERATURE": 0.8,
    "MAX_TOKENS": 500,
    "PRESENCE_PENALTY": 0.6,
    "FREQUENCY_PENALTY": 0.6
}