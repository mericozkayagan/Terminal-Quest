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

### Save System

- Save and load game functionality with up to 5 save slots
- PostgreSQL database for persistent storage
- Docker-based database setup for easy deployment
- Start menu with New Game and Load Game options
- Character and inventory data persistence
- Automatic saving before exiting the game

## Installation

### Prerequisites

- Python 3.12+
- OpenAI API key (for AI-generated content)
- Docker and Docker Compose (for the save system)

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

4. Start the game with database (recommended):

```bash
./start.sh
```

5. Or run without the automated setup:

```bash
# Start the database
docker-compose up -d
# Run the game
python3 main.py
```

## Project Structure

```
terminal_quest/
├── src/                    # Source code
│   ├── models/            # Game entities and data structures
│   │   ├── character.py       # Base Character, Player, and Enemy classes
│   │   ├── character_classes.py # Character class definitions
│   │   ├── items/             # Item system implementation
│   │   ├── skills.py          # Skill system
│   │   └── status_effects.py  # Status effects system
│   ├── services/          # Game systems
│   │   ├── ai_generator.py    # OpenAI integration
│   │   ├── combat.py          # Combat system
│   │   ├── shop.py            # Shop system
│   │   ├── character_creation.py # Character creation system
│   │   ├── character_storage.py # Character storage for saves
│   │   └── save_manager.py    # Save game management
│   ├── display/           # Display views
│   │   ├── main/             # Main game display
│   │   ├── inventory/        # Inventory display
│   │   ├── combat/           # Combat display
│   │   ├── shop/             # Shop display
│   │   ├── save/             # Save/load display
│   │   └── common/           # Common display components
│   ├── utils/             # Utilities
│   └── config/            # Configuration
│       ├── settings.py       # Game settings and constants
│       └── database.py       # Database configuration
├── data/                  # Game data
├── docker-compose.yml     # Docker Compose configuration
├── main.py                # Game entry point
├── start.sh               # Start script for the game
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables
└── .gitignore
```

## Docker Usage

The game uses Docker to run a PostgreSQL database for saving and loading game progress:

1. Start the database container:

```bash
docker-compose up -d
```

2. Stop the database container when not in use:

```bash
docker-compose down
```

3. Check the database container status:

```bash
docker-compose ps
```

4. Reset all save data (caution - this will erase all saves):

```bash
docker-compose down -v && docker-compose up -d
```
