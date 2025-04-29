from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import uuid


@dataclass
class NPCQuest:
    """Represents a quest that can be provided by an NPC"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    objective: str = ""
    reward_gold: int = 0
    reward_exp: int = 0
    reward_item_id: Optional[str] = None
    completed: bool = False
    progress: int = 0
    required_progress: int = 1  # Default is single objective
    available_at_level: int = 1
    requires_quest_id: Optional[str] = None  # Prerequisite quest ID


@dataclass
class NPCDialogue:
    """Dialogue tree for an NPC"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    text: str = ""
    responses: List[Dict[str, Any]] = field(default_factory=list)
    is_quest_dialogue: bool = False
    quest_id: Optional[str] = None


@dataclass
class NPC:
    """Represents an NPC in the game world"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    lore: str = ""
    ascii_art: str = ""
    faction: str = "Neutral"
    level: int = 1

    # Dialogue and quests
    default_greeting: str = "Hello there, traveler."
    dialogues: List[NPCDialogue] = field(default_factory=list)
    quests: List[NPCQuest] = field(default_factory=list)

    # NPC memory of interactions
    memory: List[str] = field(default_factory=list)
    has_met_player: bool = False
    relationship: int = 0  # -100 to 100

    def get_dialogue_by_id(self, dialogue_id: str) -> Optional[NPCDialogue]:
        """Get a dialogue by its ID"""
        for dialogue in self.dialogues:
            if dialogue.id == dialogue_id:
                return dialogue
        return None

    def get_quest_by_id(self, quest_id: str) -> Optional[NPCQuest]:
        """Get a quest by its ID"""
        for quest in self.quests:
            if quest.id == quest_id:
                return quest
        return None

    def get_available_quests(self, player_level: int) -> List[NPCQuest]:
        """Get quests available to the player based on level and prerequisites"""
        available_quests = []
        for quest in self.quests:
            if quest.completed:
                continue

            if quest.available_at_level > player_level:
                continue

            if quest.requires_quest_id:
                prerequisite_complete = False
                for q in self.quests:
                    if q.id == quest.requires_quest_id and q.completed:
                        prerequisite_complete = True
                        break
                if not prerequisite_complete:
                    continue

            available_quests.append(quest)
        return available_quests

    def add_to_memory(self, event: str) -> None:
        """Add an event to the NPC's memory"""
        self.memory.append(event)
        # Keep memory limited to last 10 events
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]

    def update_relationship(self, amount: int) -> None:
        """Update the NPC's relationship with the player"""
        self.relationship = max(-100, min(100, self.relationship + amount))

    def get_greeting(self) -> str:
        """Get appropriate greeting based on relationship and previous meetings"""
        if not self.has_met_player:
            self.has_met_player = True
            return self.default_greeting

        if self.relationship >= 50:
            return f"Ah, good to see you again, friend! What brings you back to me?"
        elif self.relationship <= -50:
            return f"You again? What do you want this time?"
        else:
            return f"Hello again. What can I do for you today?"
