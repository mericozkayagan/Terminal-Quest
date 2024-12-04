# Dark fantasy theme constants
SYMBOLS = {
    "HEALTH": "❥",  # Gothic heart
    "MANA": "✠",  # Dark cross
    "ATTACK": "⚔",  # Crossed swords
    "DEFENSE": "◈",  # Shield
    "GOLD": "⚜",  # Fleur-de-lis
    "EXP": "✧",  # Soul essence
    "WEAPON": "🗡",  # Dagger
    "ARMOR": "🛡",  # Shield
    "ACCESSORY": "⚝",  # Mystical star
    "MARKET": "⚖",  # Scales
    "MEDITATION": "✤",  # Spirit flower
    "EQUIPMENT": "⚒",  # Tools
    "CURSOR": "◆",  # Diamond
    "RUNE": "ᛟ",  # Norse rune
    "SKULL": "☠",  # Death
    "POTION": "⚱",  # Vial
    "CURSE": "⛧",  # Pentagram
    "SOUL": "❦",  # Soul marker
}

# Atmospheric elements
DECORATIONS = {
    "TITLE": {"PREFIX": "⚝ • ✧ • ", "SUFFIX": " • ✧ • ⚝"},
    "SECTION": {"START": "┄┄ ", "END": " ┄┄"},
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
