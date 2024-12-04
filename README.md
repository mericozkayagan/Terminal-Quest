# Terminal Quest

A sophisticated text-based RPG that leverages AI to generate unique content, featuring dynamic character classes, items, and a complex combat system with status effects.

## Features

### AI-Powered Content Generation
- Dynamic character class generation using OpenAI's GPT-3.5
- Intelligent fallback system with predefined classes (Plague Herald, Blood Sovereign, Void Harbinger)
- Balanced stat generation within predefined ranges
- Unique skill and ability creation

### Advanced Combat System
- Turn-based tactical combat with status effects
- Equipment-based stat modifications
- Skill system with mana management
- Status effects that modify stats and deal damage over time:
  - Bleeding: Continuous damage (5 damage/turn)
  - Poisoned: Damage + attack reduction (3 damage/turn, -2 attack)
  - Weakened: Reduced combat stats (-3 attack, -2 defense)
  - Burning: High damage over time (7 damage/turn)
  - Cursed: Multi-stat reduction (-2 attack, -1 defense, -10 mana)

### Comprehensive Item System
- Multiple item types:
  - Weapons with attack modifiers
  - Armor with defense and health bonuses
  - Accessories with unique stat combinations
  - Consumables with healing and status effects
- Durability system for equipment (40-100 based on rarity)
- Rarity system (Common to Legendary) with drop chances:
  - Common: 15%
  - Uncommon: 10%
  - Rare: 5%
  - Epic: 3%
  - Legendary: 1%
- Dynamic shop system with item descriptions and stats

### Character Classes
- Plague Herald: Disease and decay specialist (90 HP, 14 ATK, 4 DEF, 80 MP)
- Blood Sovereign: Vampiric powers and blood magic (100 HP, 16 ATK, 5 DEF, 70 MP)
- Void Harbinger: Cosmic void manipulation (85 HP, 12 ATK, 3 DEF, 100 MP)
- AI-generated custom classes within balanced stat ranges

### Character Progression
- Experience-based leveling system
- Level-up bonuses:
  - Health: +20
  - Mana: +15
  - Attack: +5
  - Defense: +3
- Equipment management with three slots (weapon, armor, accessory)
- Inventory system with consumables and equipment
- Gold-based economy with configurable sell prices

## Installation

### Prerequisites
- Python 3.12+
- OpenAI API key (for AI-generated content)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/terminal-quest.git
cd terminal-quest
```
2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Create a `.env` file:
```env
OPENAI_API_KEY=your_key_here
```

4. Run the game:
```bash
python3 main.py
```

## Project Structure

```
terminal_quest/
├── src/                    # Source code
│   ├── models/            # Game entities and data structures
│   │   ├── character.py       # Base Character, Player, and Enemy classes
│   │   ├── character_classes.py # Character class definitions
│   │   ├── items.py           # Item system implementation
│   │   ├── skills.py          # Skill system
│   │   └── status_effects.py  # Status effects system
│   ├── services/          # Game systems
│   │   ├── ai_generator.py    # OpenAI integration
│   │   ├── combat.py          # Combat system
│   │   └── shop.py           # Shop system
│   ├── utils/             # Utilities
│   │   └── display.py        # UI utilities
│   └── config/            # Configuration
│       └── settings.py       # Game settings and constants
├── data/                  # Game data
│   ├── items.json         # Item definitions
│   └── fallbacks.json     # Fallback content
├── main.py               # Game entry point
├── requirements.txt      # Project dependencies
├── .env                 # Environment variables
└── .gitignore
```

## Best Practices

### Code Organization
- Modular design with clear separation of concerns
- Configuration centralized in settings.py
- Type hints throughout the codebase
- Comprehensive documentation and comments

### Error Handling
- Graceful fallback system for AI failures
- Input validation for all user interactions
- Proper exception handling for file and API operations

### Game Balance
- Configurable game constants in settings.py
- Balanced stat ranges for characters and items
- Progressive difficulty scaling
- Fair item drop rates and shop prices

### Performance
- Efficient status effect processing
- Minimal API calls with caching
- Optimized combat calculations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the established code style:
   - Use type hints
   - Follow PEP 8
   - Add docstrings for functions and classes
   - Update tests if applicable
4. Submit a pull request

## Future Enhancements
- Quest system
- More character classes
- Additional status effects
- Enhanced AI integration
- Saving/loading system
- Multiplayer support

## License
This project is licensed under the MIT License - see the LICENSE file for details.