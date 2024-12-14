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
    "GOLD_PER_LEVEL": 30,
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
    "SKILL_MANA_COST": (10, 25),
    "SKILL_COOLDOWN": (1, 5),  # Example range for skill cooldowns
}

# Starting inventory
STARTING_INVENTORY = {"Gold": 100, "items": []}

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
        "LEGENDARY": 0.01,
    },
}

# Status effect settings
STATUS_EFFECT_SETTINGS = {
    "BLEEDING": {"DURATION": 3, "DAMAGE": 5, "CHANCE": 0.7},
    "POISONED": {"DURATION": 4, "DAMAGE": 3, "ATTACK_REDUCTION": 2, "CHANCE": 0.6},
    "WEAKENED": {
        "DURATION": 2,
        "ATTACK_REDUCTION": 3,
        "DEFENSE_REDUCTION": 2,
        "CHANCE": 0.8,
    },
    "BURNING": {"DURATION": 2, "DAMAGE": 7, "CHANCE": 0.65},
    "CURSED": {
        "DURATION": 3,
        "DAMAGE": 2,
        "ATTACK_REDUCTION": 2,
        "DEFENSE_REDUCTION": 1,
        "MANA_REDUCTION": 10,
        "CHANCE": 0.5,
    },
}

# Display settings
DISPLAY_SETTINGS = {
    "TYPE_SPEED": 0.03,
    "COMBAT_MESSAGE_DELAY": 1.0,
    "LEVEL_UP_DELAY": 2.0,
}

# AI Generation settings
AI_SETTINGS = {
    "TEMPERATURE": 0.7,
    "MAX_TOKENS": 800,
    "MAX_RETRIES": 3,
    "PRESENCE_PENALTY": 0.2,
    "FREQUENCY_PENALTY": 0.3,
    "TIMEOUT": 30,
}

# AI Generation Settings
ENABLE_AI_CLASS_GENERATION = False  # Enable AI generation for character classes
ENABLE_AI_ENEMY_GENERATION = True  # Enable AI generation for enemies
ENABLE_AI_ITEM_GENERATION = True  # Enable AI generation for items
ENABLE_AI_ART_GENERATION = True  # Master switch for all AI art generation

# AI Generation Retry Settings
MAX_GENERATION_ATTEMPTS = 3  # Maximum number of retry attempts for generation
GENERATION_TIMEOUT = 30  # Timeout in seconds for each generation attempt

# Enemy Generation Settings
ENEMY_GENERATION = {
    "BASE_HEALTH_RANGE": (40, 70),
    "BASE_ATTACK_RANGE": (8, 15),
    "BASE_DEFENSE_RANGE": (2, 6),
    "LEVEL_SCALING": {
        "HEALTH_PER_LEVEL": 5,
        "ATTACK_PER_LEVEL": 2,
        "DEFENSE_PER_LEVEL": 1,
    },
    "EXP_REWARD": {"BASE": 10, "MULTIPLIER": 1.0},
}

# Shop settings
SHOP_SETTINGS = {
    "ITEM_APPEARANCE_CHANCE": 0.3,
    "SELL_MULTIPLIER": 0.5,
    "REFRESH_COST": 100,
    "POST_COMBAT_EQUIPMENT_COUNT": 4,
    "SPECIAL_EVENT_CHANCE": 0.2,
    "SHOP_TYPE_WEIGHTS": {
        "GENERAL": 0.4,
        "BLACKSMITH": 0.3,
        "ALCHEMIST": 0.2,
        "MYSTIC": 0.1,
    },
    "SHOP_TYPE_BONUSES": {
        "BLACKSMITH": {"weapon": 1.2, "armor": 1.2},
        "ALCHEMIST": {"consumable": 0.8, "potion_stock": 3},
        "MYSTIC": {"set_piece_chance": 1.5},
    },
    "BASE_POTION_STOCK": {
        "GENERAL": 1,
        "ALCHEMIST": 3,
        "MYSTIC": 1,
        "BLACKSMITH": 1,
    },
    "RARITY_WEIGHTS": {
        "COMMON": 0.40,
        "UNCOMMON": 0.30,
        "RARE": 0.20,
        "EPIC": 0.08,
        "LEGENDARY": 0.02,
    },
    "SET_PIECE_CHANCE": 0.15,
    "LEVEL_SCALING": {
        "RARITY_BOOST": 0.02,  # Per player level
        "LEGENDARY_MIN_LEVEL": 20,
        "EPIC_MIN_LEVEL": 15,
    },
}

# Database configuration settings for PostgreSQL
DATABASE_SETTINGS = {
    "DB_NAME": "rpg_game",
    "DB_USER": "rpg_user",
    "DB_PASSWORD": "secure_password",
    "DB_HOST": "localhost",
    "DB_PORT": 5432,
}

# Authentication and session management settings
AUTH_SETTINGS = {
    "SESSION_TIMEOUT": 3600,  # Session timeout in seconds
    "JWT_SECRET_KEY": "your_secret_key",
    "JWT_ALGORITHM": "HS256",
    "REDIS_HOST": "localhost",
    "REDIS_PORT": 6379,
    "REDIS_DB": 0,
}
