# Terminal Quest Documentation

Terminal Quest is a text-based RPG that uses AI to generate unique content. The game features dynamic character classes, items, and combat systems.

## Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```
4. Run the game: `python main.py`

## Game Features

### Character Classes
- AI-generated unique character classes
- Each class has special skills and base stats
- Fallback classes when AI generation fails

### Combat System
- Turn-based combat
- Status effects (bleeding, poison, etc.)
- Skill-based abilities
- Random encounters
- Environmental effects such as weather conditions and terrain
- Dynamic battlefields with hazards like traps or obstacles

### Items and Equipment
- Various item types (weapons, armor, consumables)
- Equipment affects character stats
- Items can be bought in shops or dropped by enemies
- Inventory management system

### Status Effects
- Dynamic status effect system
- Effects can modify stats or deal damage over time
- Multiple effects can be active simultaneously

### ASCII Art
- AI-generated pixel art converted into ASCII art
- ASCII art stored in `data/art/` directory
- ASCII art displayed during game events such as encounters with monsters or finding items

## Project Structure
