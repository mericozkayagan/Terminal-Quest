import json
import logging
import random
from typing import Optional, Dict, List, Any
import uuid

from src.models.npc import NPC, NPCDialogue, NPCQuest
from src.services.ai_core import generate_content
from src.services.art_generator import generate_ascii_portrait

logger = logging.getLogger(__name__)

# Define world lore for context in AI prompts
WORLD_LORE = """
The world is corrupted by the twisted influence of the God of Hope. Once a benevolent deity, the God of Hope has undergone a perversion of its nature, bringing a corrupted form of hope that drives mortals to madness and despair.

Key aspects of the world:
1. The God of Hope's presence twists all it touches, corrupting beings with a perverted form of hope
2. Many former holy sites and followers are now twisted by this corruption
3. Some resist the corruption, hiding in shadows and searching for ways to cleanse the realm
4. Ancient beings have awakened due to the corruption's spread
5. The world is in a state of decay, with pockets of resistance fighting against the God of Hope's influence
6. Those who embrace the corrupted hope gain power but lose their sanity and humanity
7. Ruins of once-great civilizations dot the landscape, now haunted by corrupted entities
8. Strange phenomena occur where reality itself seems to bend to the corrupted hope's influence
9. The concept of true hope has been tainted, making genuine optimism rare and precious
"""


class NPCGenerator:
    """Handles generation of NPCs with AI assistance"""

    @staticmethod
    def generate_npc(player_level: int, faction: str = None) -> Optional[NPC]:
        """Generate a complete NPC with AI assistance"""
        try:
            # Generate basic NPC data
            npc_data = NPCGenerator._generate_npc_data(player_level, faction)
            if not npc_data:
                logger.error("Failed to generate NPC data")
                return None

            # Create NPC instance
            npc = NPC(
                id=str(uuid.uuid4()),
                name=npc_data.get("name", "Unknown"),
                description=npc_data.get("description", ""),
                lore=npc_data.get("lore", ""),
                faction=npc_data.get("faction", "Neutral"),
                level=npc_data.get("level", player_level),
            )

            # Generate ASCII art for the NPC
            npc.ascii_art = NPCGenerator._generate_npc_art(npc.name, npc.description)

            # Generate default greeting
            npc.default_greeting = npc_data.get("greeting", "Hello there, traveler.")

            # Generate dialogues
            dialogues_data = NPCGenerator._generate_npc_dialogues(npc.name, npc.lore)
            if dialogues_data:
                for dialogue_data in dialogues_data:
                    dialogue = NPCDialogue(
                        id=str(uuid.uuid4()),
                        text=dialogue_data.get("text", ""),
                        responses=[
                            {
                                "text": response.get("text", ""),
                                "next_dialogue": None,
                                "action": response.get("action", ""),
                                "relationship_change": response.get(
                                    "relationship_change", 0
                                ),
                            }
                            for response in dialogue_data.get("responses", [])
                        ],
                    )
                    npc.dialogues.append(dialogue)

            # Generate quests if appropriate for the NPC
            if random.random() < 0.7:  # 70% chance for NPC to have quests
                quests_data = NPCGenerator._generate_npc_quests(
                    npc.name, npc.lore, player_level
                )
                if quests_data:
                    for quest_data in quests_data:
                        quest = NPCQuest(
                            id=str(uuid.uuid4()),
                            name=quest_data.get("name", "Unknown Quest"),
                            description=quest_data.get("description", ""),
                            objective=quest_data.get("objective", ""),
                            reward_gold=quest_data.get(
                                "reward_gold", random.randint(10, 50) * player_level
                            ),
                            reward_exp=quest_data.get(
                                "reward_exp", random.randint(20, 100) * player_level
                            ),
                            required_progress=quest_data.get("required_progress", 1),
                            available_at_level=quest_data.get(
                                "min_level", player_level
                            ),
                        )
                        npc.quests.append(quest)

                        # Create quest dialogue
                        quest_dialogue = NPCDialogue(
                            id=str(uuid.uuid4()),
                            text=quest_data.get(
                                "dialogue",
                                f"I need help with something: {quest.description}",
                            ),
                            responses=[
                                {
                                    "text": "I'll help you with this task.",
                                    "action": "accept_quest",
                                    "quest_id": quest.id,
                                    "relationship_change": 10,
                                },
                                {
                                    "text": "Not interested at the moment.",
                                    "action": "decline_quest",
                                    "relationship_change": -5,
                                },
                            ],
                            is_quest_dialogue=True,
                            quest_id=quest.id,
                        )
                        npc.dialogues.append(quest_dialogue)

            return npc

        except Exception as e:
            logger.error(f"Error generating NPC: {str(e)}")
            return None

    @staticmethod
    def _generate_npc_data(
        player_level: int, faction: str = None
    ) -> Optional[Dict[str, Any]]:
        """Generate basic NPC data using AI"""
        factions = ["Corrupted", "Resistance", "Neutral", "Transformed"]
        if not faction:
            faction = random.choice(factions)

        prompt = f"""Generate a unique NPC for a dark fantasy game where the world is corrupted by the God of Hope.

Player Level: {player_level}
NPC Faction: {faction}

World Context:
{WORLD_LORE}

Return JSON with:
{{
  "name": "NPC name",
  "description": "Physical description (1-2 sentences)",
  "lore": "NPC backstory (2-3 sentences)",
  "faction": "{faction}",
  "level": "NPC level (number close to player level)",
  "greeting": "NPC's first greeting to player (1 sentence)"
}}

Make the NPC appropriate for the faction:
- Corrupted: Influenced by the God of Hope, showing signs of corruption
- Resistance: Fighting against the God of Hope's influence
- Neutral: Trying to survive in this broken world
- Transformed: Changed by corruption but not entirely lost

IMPORTANT: The description, lore, and greeting should reflect the NPC's perspective on this corrupted world."""

        content = generate_content(prompt)
        if not content:
            return None

        try:
            data = json.loads(content)

            # Ensure level is an integer
            if "level" in data and not isinstance(data["level"], int):
                try:
                    data["level"] = int(data["level"])
                except ValueError:
                    data["level"] = player_level

            return data
        except Exception as e:
            logger.error(f"Error parsing NPC data: {str(e)}")
            return None

    @staticmethod
    def _generate_npc_art(name: str, description: str) -> str:
        """Generate detailed ASCII art for the NPC"""
        try:
            # Create a more detailed portrait for the NPC
            art = generate_ascii_portrait(name, description)
            return art
        except Exception as e:
            logger.error(f"Error generating NPC portrait: {str(e)}")

            # Fallback art if generation fails
            return """
╔═══════════════════════════════╗
║         ▄▄█████▄▄             ║
║      ▄█▀▀░░░░░░░▀▀█▄          ║
║     ██░▒▓████████▓▒░██        ║
║    ██░▓█▀╔══╗╔══╗▀█▓░██       ║
║    █▓▒█╔══║██║══╗█▒▓█         ║
║    █▓▒█║◆═╚══╝═◆║█▒▓█         ║
║    ██▓█╚════════╝█▓██         ║
║     ███▀▀══════▀▀███          ║
║    ██╱▓▓▓██████▓▓▓╲██         ║
║   ██▌║▓▓▓▓▀██▀▓▓▓▓║▐██        ║
║   ██▌║▓▓▓▓░██░▓▓▓▓║▐██        ║
║    ██╲▓▓▓▓░██░▓▓▓▓╱██         ║
║     ███▄▄░████░▄▄███          ║
╚═══════════════════════════════╝
"""

    @staticmethod
    def _generate_npc_dialogues(
        npc_name: str, npc_lore: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Generate dialogue options for the NPC"""
        prompt = f"""Create dialogue options for an NPC named {npc_name} in a dark fantasy world corrupted by the God of Hope.

NPC Background:
{npc_lore}

World Context:
{WORLD_LORE}

Generate 3 unique dialogue paths that the player might discuss with this NPC. Each should have 3 player response options.

Return a JSON array with:
[
  {{
    "text": "What the NPC says",
    "responses": [
      {{
        "text": "Player response option 1",
        "action": "describe what happens (information gained, etc.)",
        "relationship_change": number from -10 to +10
      }},
      {{
        "text": "Player response option 2",
        "action": "describe what happens",
        "relationship_change": number from -10 to +10
      }},
      {{
        "text": "Player response option 3",
        "action": "describe what happens",
        "relationship_change": number from -10 to +10
      }}
    ]
  }},
  ... (2 more dialogue objects)
]

Make dialogues thematically consistent with the dark fantasy setting and the NPC's background."""

        content = generate_content(prompt)
        if not content:
            return None

        try:
            data = json.loads(content)
            return data
        except Exception as e:
            logger.error(f"Error parsing NPC dialogues: {str(e)}")
            return None

    @staticmethod
    def _generate_npc_quests(
        npc_name: str, npc_lore: str, player_level: int
    ) -> Optional[List[Dict[str, Any]]]:
        """Generate quests that the NPC can offer"""
        prompt = f"""Create 1-2 quests that NPC {npc_name} can offer the player in a dark fantasy world corrupted by the God of Hope.

NPC Background:
{npc_lore}

Player Level: {player_level}

World Context:
{WORLD_LORE}

Return a JSON array with:
[
  {{
    "name": "Quest name",
    "description": "What the quest is about (1-2 sentences)",
    "objective": "What the player must do to complete it",
    "dialogue": "How the NPC asks the player to do this quest",
    "reward_gold": number (appropriate for player level),
    "reward_exp": number (appropriate for player level),
    "required_progress": number (how many things to collect/defeat),
    "min_level": number (minimum player level, close to current)
  }},
  ... (optional second quest)
]

The quests should:
1. Make sense for this NPC to offer based on their background
2. Fit the dark, corrupted theme of the world
3. Have reasonable rewards for the player's level
4. Include activities like gathering corrupted items, defeating enemies, finding lost individuals, etc."""

        content = generate_content(prompt)
        if not content:
            return None

        try:
            data = json.loads(content)
            return data
        except Exception as e:
            logger.error(f"Error parsing NPC quests: {str(e)}")
            return None

    @staticmethod
    def generate_npc_response(
        npc: NPC, player_input: str, conversation_history: List[str]
    ) -> str:
        """Generate a dynamic response from the NPC to player input"""
        # Format conversation history
        history_text = (
            "\n".join(conversation_history[-5:])
            if conversation_history
            else "No previous conversation."
        )

        prompt = f"""Generate a response from NPC {npc.name} to the player's input in a dark fantasy RPG.

NPC Information:
Name: {npc.name}
Description: {npc.description}
Background: {npc.lore}
Faction: {npc.faction}
Relationship with player: {"Positive" if npc.relationship > 20 else "Negative" if npc.relationship < -20 else "Neutral"}

World Context:
{WORLD_LORE}

Recent Conversation:
{history_text}

Player's Input: "{player_input}"

Generate a single in-character response from {npc.name} that:
1. Maintains the NPC's personality and speaking style
2. Acknowledges the player's input
3. Fits the dark fantasy setting
4. Reflects the NPC's faction and background
5. Keeps dialogue concise (1-3 sentences)

Return ONLY the NPC's dialogue response as plain text with no markup or quotation marks."""

        content = generate_content(prompt)
        if not content:
            return f"{npc.name} stares at you silently."

        return content.strip("\"')")
