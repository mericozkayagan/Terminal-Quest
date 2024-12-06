"""Dark theme constants and decorations for the game"""

SYMBOLS = {
    "HEALTH": "♥",  # Classic RPG heart
    "MANA": "✦",  # Magic star
    "ATTACK": "⚔",  # Crossed swords
    "DEFENSE": "⛊",  # Shield
    "GOLD": "⚜",  # Treasure
    "EXP": "✵",  # Experience star
    "WEAPON": "⚒",  # Weapon
    "ARMOR": "⛨",  # Armor
    "ACCESSORY": "❈",  # Accessory
    "MARKET": "⚖",  # Market scales
    "MEDITATION": "❋",  # Rest symbol
    "EQUIPMENT": "⚔",  # Equipment
    "CURSOR": "➤",  # Selection arrow
    "RUNE": "ᛟ",  # Magical rune
    "SKULL": "☠",  # Death
    "POTION": "⚱",  # Potion vial
    "CURSE": "⚉",  # Curse symbol
    "SOUL": "❂",  # Soul essence
    "SKILL": "✤",  # Add this line
}

DECORATIONS = {
    "TITLE": {"PREFIX": "ᚷ • ✧ • ", "SUFFIX": " • ✧ • ᚷ"},
    "SECTION": {"START": "┄┄ ", "END": " ┄┄"},
    "ERROR": {"START": "⚠ ", "END": " ⚠"},
    "SEPARATOR": "✧──────────────────────✧",
    "SMALL_SEP": "• • •",
    "RUNES": ["ᚱ", "ᚨ", "ᚷ", "ᚹ", "ᛟ", "ᚻ", "ᚾ", "ᛉ", "ᛋ"],
}

# Display formatting
FORMATS = {
    "TITLE": "{prefix}{text}{suffix}",
    "SECTION": "\n{dec_start}{text}{dec_end}",
    "STAT": "  {symbol} {label:<12} {value}",
    "ITEM": "  {cursor} {name:<25} {details}",
    "ACTION": "  {cursor} {number}  {text}",
}

# Standard widths
WIDTHS = {"TOTAL": 60, "LABEL": 12, "VALUE": 20, "NAME": 25, "DESC": 40}
