from typing import Optional, Dict, List, Any, Tuple
import random
import logging
from src.models.character import Player, Enemy
from src.services.ai_generator import generate_enemy
from src.services.ai_core import generate_content
from src.models.items.base import Item
from src.models.base_types import EncounterType
from src.utils.json_cleaner import JSONCleaner
from src.services.npc_generator import NPCGenerator
import json
from enum import Enum, auto
import os

logger = logging.getLogger(__name__)


class EncounterType(Enum):
    COMBAT = auto()
    PUZZLE = auto()
    TREASURE = auto()
    TRAP = auto()
    NPC = auto()
    BOSS = auto()


class EncounterService:
    """
    Handles the generation and management of game encounters.
    Tracks encounter frequency and determines when boss encounters should occur.
    Implemented as a Singleton to ensure consistency across the application.
    """

    # Singleton instance
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EncounterService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, boss_threshold: int = 10):
        # Only initialize once
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.encounter_count = 0
        self.boss_threshold = (
            boss_threshold  # Deprecated, boss timing now uses interval
        )
        self.encounter_history = []
        self.encounter_types = [
            EncounterType.COMBAT,
            EncounterType.PUZZLE,
            EncounterType.TREASURE,
            EncounterType.TRAP,
            EncounterType.NPC,
        ]

        # Read boss interval from environment variable
        try:
            # Default to 8 if not set or invalid
            self._boss_interval_setting = int(os.getenv("BOSS_ENCOUNTER_INTERVAL", 8))
            if self._boss_interval_setting <= 0:
                logger.warning(
                    f"Invalid BOSS_ENCOUNTER_INTERVAL '{os.getenv('BOSS_ENCOUNTER_INTERVAL')}', using default 8."
                )
                self._boss_interval_setting = 8
        except ValueError:
            logger.warning(
                f"Invalid BOSS_ENCOUNTER_INTERVAL '{os.getenv('BOSS_ENCOUNTER_INTERVAL')}', using default 8."
            )
            self._boss_interval_setting = 8

        # Track progress toward boss encounters using the setting
        self.encounters_until_boss = self._generate_boss_interval()
        self.total_boss_interval = self.encounters_until_boss
        logger.info(
            f"Initialized boss counter: {self.encounters_until_boss}/{self.total_boss_interval} (Interval Setting: {self._boss_interval_setting})"
        )

        # NPC generator service
        self.npc_generator = NPCGenerator()

        self._initialized = True

    def reset_boss_counter(self):
        """Reset the boss encounter counter after a boss fight or loading game."""
        self.encounters_until_boss = self._generate_boss_interval()
        self.total_boss_interval = self.encounters_until_boss
        logger.info(
            f"Reset boss counter: {self.encounters_until_boss}/{self.total_boss_interval}"
        )

    def get_next_encounter(self, player: Player) -> Dict[str, Any]:
        """Generate the next encounter based on player's status and encounter history"""
        self.encounter_count += 1

        # Add small chance for treasure or puzzle after combat encounters
        weights = self._calculate_encounter_weights()

        # Select encounter type based on weights
        encounter_type = random.choices(self.encounter_types, weights=weights, k=1)[0]

        # Generate encounter based on type
        if encounter_type == EncounterType.COMBAT:
            return self._generate_combat_encounter(player)
        elif encounter_type == EncounterType.PUZZLE:
            return self._generate_puzzle_encounter(player)
        elif encounter_type == EncounterType.TREASURE:
            return self._generate_treasure_encounter(player)
        elif encounter_type == EncounterType.TRAP:
            return self._generate_trap_encounter(player)
        elif encounter_type == EncounterType.NPC:
            return self._generate_npc_encounter(player)
        elif encounter_type == EncounterType.BOSS:
            return self._generate_boss_encounter(player)
        else:
            # Fallback to combat
            return self._generate_combat_encounter(player)

    def should_spawn_boss(self) -> bool:
        """Check if it's time for a boss encounter"""
        # Boss threshold is a range of encounters (e.g., 10-15)
        min_threshold = self.boss_threshold
        max_threshold = self.boss_threshold + 5

        if self.encounter_count >= min_threshold:
            # Increasing chance of boss encounter after min_threshold
            chance = min(0.95, (self.encounter_count - min_threshold + 1) * 0.2)
            if random.random() < chance or self.encounter_count >= max_threshold:
                self.encounter_count = 0  # Reset counter after boss
                return True
        return False

    def reset_counter(self):
        """Reset the encounter counter"""
        self.encounter_count = 0

    def _calculate_encounter_weights(self) -> List[float]:
        """Calculate weights for each encounter type based on history"""
        # Default weights
        weights = [60, 5, 10, 5, 20]  # Combat, Puzzle, Treasure, Trap, NPC

        # Adjust weights based on recent encounters
        if len(self.encounter_history) > 0:
            last_encounter = self.encounter_history[-1]

            # If last encounter was combat, increase chance of non-combat
            if last_encounter == EncounterType.COMBAT:
                weights = [50, 15, 20, 5, 10]  # Reduce combat, increase others

            # If player had several combat encounters in a row, increase treasure chance
            if len(self.encounter_history) >= 3:
                if all(e == EncounterType.COMBAT for e in self.encounter_history[-3:]):
                    weights = [40, 15, 30, 5, 10]  # Higher treasure chance

        return weights

    def _generate_combat_encounter(self, player: Player) -> Dict[str, Any]:
        """Generate a combat encounter"""
        enemy = generate_enemy(player.level)
        self.encounter_history.append(EncounterType.COMBAT)

        return {
            "type": EncounterType.COMBAT,
            "enemy": enemy,
            "description": f"You encounter {enemy.name}. The air feels tense as it prepares to attack.",
        }

    def _generate_puzzle_encounter(self, player: Player) -> Dict[str, Any]:
        """Generate a puzzle encounter using AI"""
        self.encounter_history.append(EncounterType.PUZZLE)

        # AI-generated puzzle
        prompt = """Create a short, atmospheric puzzle encounter for a dark fantasy RPG.

The player is exploring a world corrupted by the God of Hope.

Return a JSON object with:
1. A brief description of the puzzle scene
2. The puzzle itself (riddle, pattern, etc.)
3. The solution
4. A reward (small amount of gold, minor item, or small HP/mana boost)
5. 2-3 hints that can be provided if player struggles

FORMAT:
{
  "scene": "description of what the player encounters",
  "puzzle": "the actual puzzle/riddle text",
  "solution": "the answer or method to solve it",
  "reward": {"type": "gold|health|mana|exp", "amount": 10-30},
  "hints": ["hint1", "hint2"]
}"""

        content = generate_content(prompt)
        if not content:
            return self._generate_fallback_puzzle()

        try:
            data = json.loads(content)
            return {
                "type": EncounterType.PUZZLE,
                "scene": data["scene"],
                "puzzle": data["puzzle"],
                "solution": data["solution"],
                "reward": data["reward"],
                "hints": data["hints"],
            }
        except Exception as e:
            logger.error(f"Error parsing puzzle encounter: {str(e)}")
            return self._generate_fallback_puzzle()

    def _generate_treasure_encounter(self, player: Player) -> Dict[str, Any]:
        """Generate a treasure encounter"""
        self.encounter_history.append(EncounterType.TREASURE)

        # Calculate gold based on player level
        gold_amount = random.randint(player.level * 10, player.level * 25)

        # Chance for an item with the gold
        has_item = random.random() < 0.4

        prompt = f"""Create a detailed description of a hidden treasure the player discovers in a dark fantasy world.
The world is corrupted by twisted hope, so treasure can be found in unusual or unsettling places.
The treasure contains {gold_amount} gold coins.

Return a JSON object with:
{{
  "description": "atmospheric 2-3 sentence description of finding the treasure"
}}"""

        content = generate_content(prompt)
        treasure_desc = "You found a small hidden cache of treasure."

        if content:
            try:
                data = json.loads(content)
                treasure_desc = data["description"]
            except:
                pass

        return {
            "type": EncounterType.TREASURE,
            "description": treasure_desc,
            "gold": gold_amount,
            "has_item": has_item,
        }

    def _generate_trap_encounter(self, player: Player) -> Dict[str, Any]:
        """Generate a trap encounter"""
        self.encounter_history.append(EncounterType.TRAP)

        # Calculate damage based on player level (not too punishing)
        damage = random.randint(
            int(player.max_health * 0.05), int(player.max_health * 0.15)
        )

        # AI-generated trap description
        prompt = f"""Create a detailed description of a trap the player encounters in a dark fantasy world.
The world is corrupted by twisted hope. The trap will cause {damage} damage.

Return a JSON object with:
{{
  "description": "atmospheric 2-3 sentence description of the trap",
  "triggered_text": "what happens when the trap is triggered",
  "evaded_text": "what happens if the player successfully evades"
}}"""

        content = generate_content(prompt)
        if not content:
            return {
                "type": EncounterType.TRAP,
                "description": "You notice something suspicious ahead.",
                "triggered_text": f"A hidden trap springs, dealing {damage} damage!",
                "evaded_text": "You carefully avoid the trap mechanism.",
                "damage": damage,
                "difficulty": player.level + random.randint(1, 5),
            }

        try:
            data = json.loads(content)
            return {
                "type": EncounterType.TRAP,
                "description": data["description"],
                "triggered_text": data["triggered_text"],
                "evaded_text": data["evaded_text"],
                "damage": damage,
                "difficulty": player.level + random.randint(1, 5),
            }
        except Exception as e:
            logger.error(f"Error parsing trap encounter: {str(e)}")
            return {
                "type": EncounterType.TRAP,
                "description": "You notice something suspicious ahead.",
                "triggered_text": f"A hidden trap springs, dealing {damage} damage!",
                "evaded_text": "You carefully avoid the trap mechanism.",
                "damage": damage,
                "difficulty": player.level + random.randint(1, 5),
            }

    def _generate_npc_encounter(self, player: Player) -> Dict[str, Any]:
        """Generate an NPC encounter"""
        self.encounter_history.append(EncounterType.NPC)

        # Use the NPCGenerator to create a fully-featured NPC
        npc = NPCGenerator.generate_npc(player.level)

        if not npc:
            # Fallback to simple NPC data if generation fails
            return self._generate_fallback_npc()

        return {"type": EncounterType.NPC, "npc": npc}

    def _generate_fallback_puzzle(self) -> Dict[str, Any]:
        """Generate a fallback puzzle if AI generation fails"""
        # Predefined puzzles as fallback
        puzzles = [
            {
                "scene": "You find an ancient stone tablet with symbols carved into it.",
                "puzzle": "What has keys but can't open locks, space but no room, and you can enter but not go in?",
                "solution": "keyboard",
                "reward": {"type": "gold", "amount": 15},
                "hints": [
                    "It's something you use every day",
                    "You're using it right now",
                ],
            },
            {
                "scene": "A spectral apparition blocks your path with a riddle.",
                "puzzle": "I'm light as a feather, but the strongest person can't hold me for more than a minute.",
                "solution": "breath",
                "reward": {"type": "health", "amount": 10},
                "hints": [
                    "It's something essential to life",
                    "You're doing it right now",
                ],
            },
            {
                "scene": "A series of runes glows on the wall, with symbols representing elements.",
                "puzzle": "I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me.",
                "solution": "fire",
                "reward": {"type": "mana", "amount": 15},
                "hints": [
                    "It's one of the classical elements",
                    "It provides light and warmth",
                ],
            },
        ]

        puzzle = random.choice(puzzles)
        puzzle["type"] = EncounterType.PUZZLE
        return puzzle

    def _generate_fallback_npc(self) -> Dict[str, Any]:
        """Generate a fallback NPC encounter if AI generation fails"""
        npcs = [
            {
                "type": EncounterType.NPC,
                "npc_name": "Wandering Merchant",
                "description": "A hunched figure with a large pack, eyes darting nervously.",
                "dialogue": "Psst! Want to trade? I've got... special items. Not cursed, I promise!",
                "options": [
                    {
                        "text": "Let's trade",
                        "outcome": "You gain a random item but lose 10 gold",
                    },
                    {
                        "text": "No thanks",
                        "outcome": "The merchant shrugs and moves on",
                    },
                    {
                        "text": "Why so nervous?",
                        "outcome": "The merchant gives you information about a nearby danger",
                    },
                ],
            },
            {
                "type": EncounterType.NPC,
                "npc_name": "Lost Scholar",
                "description": "A disheveled person in tattered robes, clutching a book.",
                "dialogue": "Oh! A living soul! Please, I need help with my research on Hope's corruption.",
                "options": [
                    {
                        "text": "Offer assistance",
                        "outcome": "The scholar teaches you something, +5 XP",
                    },
                    {"text": "Ignore them", "outcome": "You continue on your way"},
                    {
                        "text": "Ask about their research",
                        "outcome": "They share valuable information about boss weaknesses",
                    },
                ],
            },
        ]

        return random.choice(npcs)

    def _generate_boss_interval(self) -> int:
        """Return the configured boss interval."""
        # Use the value read during __init__
        return self._boss_interval_setting

    def get_boss_progress(self) -> Dict[str, int]:
        """Get information about progress toward the next boss encounter"""
        # Ensure we have valid values for calculation
        if self.total_boss_interval <= 0:
            # Reset if values are invalid
            self.encounters_until_boss = self._generate_boss_interval()
            self.total_boss_interval = self.encounters_until_boss
            logger.warning("Reset invalid boss progress values")

        # Calculate progress percentage
        progress_percentage = int(
            (
                (self.total_boss_interval - self.encounters_until_boss)
                / self.total_boss_interval
            )
            * 100
        )

        # Log current state
        logger.info(
            f"Boss progress: {self.encounters_until_boss}/{self.total_boss_interval} remaining ({progress_percentage}%)"
        )

        return {
            "encounters_until_boss": self.encounters_until_boss,
            "total_boss_interval": self.total_boss_interval,
            "progress_percentage": progress_percentage,
        }

    def generate_encounter(self, player_level: int) -> Dict[str, Any]:
        """Generate a random encounter based on player level

        Args:
            player_level: The player's current level

        Returns:
            Dict containing encounter information
        """
        # Check if we've reached a boss encounter
        if self.encounters_until_boss <= 0:
            encounter_type = EncounterType.BOSS
            self.encounters_until_boss = (
                self._generate_boss_interval()
            )  # Reset for next boss
            self.total_boss_interval = self.encounters_until_boss
        else:
            # Normal encounter selection
            encounter_type = self._select_encounter_type()

            # We no longer decrement the boss counter here
            # It's now handled exclusively in EncounterHandler.handle_exploration

        # Generate the appropriate encounter
        if encounter_type == EncounterType.COMBAT:
            return self._generate_combat_encounter(player_level)
        elif encounter_type == EncounterType.PUZZLE:
            return self._generate_puzzle_encounter(player_level)
        elif encounter_type == EncounterType.TREASURE:
            return self._generate_treasure_encounter(player_level)
        elif encounter_type == EncounterType.TRAP:
            return self._generate_trap_encounter(player_level)
        elif encounter_type == EncounterType.NPC:
            return self._generate_npc_encounter(player_level)
        elif encounter_type == EncounterType.BOSS:
            return self._generate_boss_encounter(player_level)
        else:
            # Default to combat if something goes wrong
            logger.error(f"Unknown encounter type: {encounter_type}")
            return self._generate_combat_encounter(player_level)

    def _select_encounter_type(self) -> EncounterType:
        """Select a random encounter type based on weighted probabilities"""
        weights = [60, 5, 10, 5, 20]  # Combat, Puzzle, Treasure, Trap, NPC
        encounter_types = [
            EncounterType.COMBAT,
            EncounterType.PUZZLE,
            EncounterType.TREASURE,
            EncounterType.TRAP,
            EncounterType.NPC,
        ]

        return random.choices(encounter_types, weights=weights, k=1)[0]

    def _generate_boss_encounter(self, player_level: int) -> Dict[str, Any]:
        """Generate a boss encounter"""
        # Boss is typically stronger than regular enemies
        boss_level = min(player_level + 2, 10)
        boss = self._generate_boss_enemy(boss_level)

        return {
            "type": EncounterType.BOSS,
            "enemies": [boss],
            "description": f"A powerful {boss.name} blocks your path. You sense the corruption of the God of Hope flowing through it.",
        }

    def _generate_boss_enemy(self, boss_level: int) -> Enemy:
        """Generate a powerful boss enemy"""
        boss_types = [
            "Archbishop of False Hope",
            "The Beckoning Light",
            "Golden Apostle",
            "Radiance Incarnate",
            "Hope's Harbinger",
            "The Blinding Truth",
            "Luminous Horror",
            "Prophet of the Golden God",
            "Corrupted Seraph",
        ]

        boss_name = random.choice(boss_types)

        # Boss stats are significantly higher than regular enemies
        health = random.randint(70, 100) * boss_level
        attack = random.randint(12, 18) * boss_level
        defense = random.randint(8, 12) * boss_level

        description = self._generate_boss_description(boss_name)

        return Enemy(
            name=boss_name,
            level=boss_level,
            health=health,
            max_health=health,
            attack=attack,
            defense=defense,
            description=description,
            is_boss=True,
        )

    def _generate_boss_description(self, boss_name: str) -> str:
        """Generate a description for a boss enemy"""
        descriptions = {
            "Archbishop of False Hope": "Once the highest servant of the true gods, now the foremost preacher of the God of Hope's twisted gospel. Golden light streams from their eyes and mouth as they speak blasphemous sermons.",
            "The Beckoning Light": "A colossal being composed entirely of corrupted golden energy, taking a vaguely humanoid form that constantly shifts and pulses. It draws in all who gaze upon it with promises of salvation.",
            "Golden Apostle": "A perfect vessel for the God of Hope's power, its human form barely contained beneath a shell of gleaming gold. Every movement releases waves of corrupting light.",
            "Radiance Incarnate": "The physical manifestation of hope's corruption, a blinding figure whose approach causes reality itself to warp and crack with golden fissures.",
            "Hope's Harbinger": "The herald of the God of Hope, chosen to prepare the way for its full arrival. Half of its body is transformed into pure golden light while the other half clings desperately to mortality.",
            "The Blinding Truth": "A being that claims to reveal the true nature of existence - a horror so profound that witnesses either go mad or submit willingly to hope's corruption.",
            "Luminous Horror": "A creature of such concentrated corrupted hope that its form can only be perceived as a silhouette within a pillar of searing golden light.",
            "Prophet of the Golden God": "The mortal voice of the God of Hope, its body a canvas of self-inflicted wounds that weep golden light as it speaks prophecies of a world consumed by 'salvation'.",
            "Corrupted Seraph": "A fallen celestial being whose divine nature has been inverted by the God of Hope, its once-protective wings now radiating malevolent golden energy that corrupts all it touches.",
        }

        # Default description if specific one not found
        return descriptions.get(
            boss_name,
            "An immensely powerful servant of the God of Hope, its very presence distorts reality with waves of corrupting golden light.",
        )
