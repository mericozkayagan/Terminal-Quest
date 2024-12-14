import random
from typing import Dict, List, Optional, Any

from .skills import Skill
from ..display.common.message_view import MessageView
from .base_types import GameEntity, EffectTrigger
from .effects.base import BaseEffect
from .items.equipment import Equipment
from .character_classes import CharacterClass
from .status_effects import StatusEffect
from ..config.settings import STARTING_INVENTORY
from .inventory import get_starting_items
from .items.sets import SetBonus, ITEM_SETS
from .base_types import ItemType
from .effects.base import BaseEffect  # Use BaseEffect instead of ItemEffect


class Character(GameEntity):
    def __init__(
        self,
        name: str,
        description: str = "",
        health: int = 100,
        attack: int = 15,
        defense: int = 5,
        level: int = 1,
    ):
        # Keep all existing initialization
        super().__init__()
        self.name = name
        self.description = description
        self.level = level

        # Combat stats
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense

        # Keep existing equipment and inventory system
        self.status_effects: Dict[str, StatusEffect] = {}
        self.equipment: Dict[str, Optional[Equipment]] = {
            "weapon": None,
            "armor": None,
            "accessory": None,
        }

        self.inventory = {
            "Gold": STARTING_INVENTORY["Gold"],
            "items": get_starting_items(),
        }

        # Effects system
        self.item_effects: List[BaseEffect] = []
        self.active_set_bonuses: Dict[str, List[SetBonus]] = {}
        self.temporary_stats: Dict[str, int] = {}
        self._effects: List[BaseEffect] = []  # New list for GameEntity effects

    # Add new methods required by GameEntity protocol
    def apply_effect(self, effect: Any) -> None:
        """Implement GameEntity protocol method"""
        if isinstance(effect, BaseEffect):
            self._effects.append(effect)
            effect.apply(self)
        elif isinstance(effect, StatusEffect):
            self.status_effects[effect.name] = effect
        elif isinstance(effect, BaseEffect):
            self.item_effects.append(effect)

    def remove_effect(self, effect: Any) -> None:
        """Implement GameEntity protocol method"""
        if isinstance(effect, BaseEffect) and effect in self._effects:
            effect.remove(self)
            self._effects.remove(effect)
        elif isinstance(effect, StatusEffect):
            effect.remove(self)
            self.status_effects.pop(effect.name, None)
        elif isinstance(effect, BaseEffect) and effect in self.item_effects:
            self.item_effects.remove(effect)

    def apply_status_effects(self):
        """Process all active status effects"""
        effects_to_remove = []
        for effect_name, effect in self.status_effects.items():
            effect.tick(self)
            effect.duration -= 1
            if effect.duration <= 0:
                effects_to_remove.append(effect_name)

        for effect_name in effects_to_remove:
            self.status_effects[effect_name].remove(self)

    def get_total_attack(self) -> int:
        """Calculate total attack including equipment bonuses"""
        total = self.attack
        for equipment in self.equipment.values():
            if equipment and isinstance(equipment.stat_modifiers, dict):
                for stat, value in equipment.stat_modifiers.items():
                    if stat == "attack":
                        total += value
        return total

    def get_total_defense(self) -> int:
        """Calculate total defense including equipment bonuses"""
        total = self.defense
        for equipment in self.equipment.values():
            if equipment and isinstance(equipment.stat_modifiers, dict):
                for stat, value in equipment.stat_modifiers.items():
                    if stat == "defense":
                        total += value
        return total

    def check_set_bonuses(self):
        """Recalculate and apply set bonuses"""
        # Remove old set bonuses
        self._remove_all_set_bonuses()

        # Count equipped set pieces
        set_counts = {}
        for item in self.equipment.values():
            if item and item.set_name:
                set_counts[item.set_name] = set_counts.get(item.set_name, 0) + 1

        # Apply new set bonuses
        for set_name, count in set_counts.items():
            item_set = ITEM_SETS.get(set_name)
            if item_set:
                active_bonuses = item_set.get_active_bonuses(count)
                self._apply_set_bonuses(set_name, active_bonuses)

    def _apply_set_bonuses(self, set_name: str, bonuses: List[SetBonus]):
        """Apply set bonuses to character"""
        self.active_set_bonuses[set_name] = bonuses

        for bonus in bonuses:
            # Apply stat bonuses
            for stat, value in bonus.stat_bonuses.items():
                current = getattr(self, stat, 0)
                setattr(self, stat, current + value)
                self.temporary_stats[stat] = self.temporary_stats.get(stat, 0) + value

            # Register bonus effects
            self.item_effects.extend(bonus.effects)

    def _remove_all_set_bonuses(self):
        """Remove all active set bonuses"""
        for set_name, bonuses in self.active_set_bonuses.items():
            for bonus in bonuses:
                # Remove stat bonuses
                for stat, value in bonus.stat_bonuses.items():
                    current = getattr(self, stat, 0)
                    setattr(self, stat, current - value)
                    self.temporary_stats[stat] = (
                        self.temporary_stats.get(stat, 0) - value
                    )

                # Remove bonus effects
                for effect in bonus.effects:
                    if effect in self.item_effects:
                        self.item_effects.remove(effect)

        self.active_set_bonuses.clear()

    def trigger_effects(
        self, trigger: EffectTrigger, target: Optional["Character"] = None
    ):
        """Trigger all effects of a specific type"""
        for effect in self.item_effects:
            if effect.trigger == trigger:
                effect.activate(self, target)


class Player(Character):
    def __init__(self, name: str, char_class: CharacterClass):
        super().__init__(
            name=name,
            description=char_class.description,
            health=char_class.base_health,
            attack=char_class.base_attack,
            defense=char_class.base_defense,
            level=1,
        )
        # Class-specific attributes
        self.char_class = char_class
        self.mana = char_class.base_mana
        self.max_mana = char_class.base_mana
        self.skills = char_class.skills

        # Progress attributes
        self.exp = 0
        self.exp_to_level = 100

        # Initialize equipment slots
        self.equipment = {"weapon": None, "armor": None, "accessory": None}

        # Session management attributes
        self.session_id = None
    
    def equip_item(self, item: "Equipment") -> bool:
        """
        Equip an item to the appropriate slot
        Returns True if successful, False otherwise
        """
        try:
            slot_mapping = {
                ItemType.WEAPON: "weapon",
                ItemType.ARMOR: "armor",
                ItemType.ACCESSORY: "accessory",
            }

            slot = slot_mapping.get(item.item_type)
            if not slot:
                MessageView.show_error(f"Cannot equip {item.name}: Invalid item type")
                return False

            if self.equipment[slot]:
                old_item = self.equipment[slot]
                for stat, value in old_item.stat_modifiers.items():
                    current = getattr(self, stat, 0)
                    setattr(self, stat, current - value)
                self.inventory["items"].append(old_item)

            self.inventory["items"].remove(item)
            self.equipment[slot] = item
            for stat, value in item.stat_modifiers.items():
                current = getattr(self, stat, 0)
                setattr(self, stat, current + value)

            MessageView.show_success(f"Equipped {item.name} to {slot}")
            return True

        except Exception as e:
            MessageView.show_error(f"Failed to equip {item.name}: {str(e)}")
            return False

    def unequip_item(self, slot: str) -> bool:
        """
        Unequip an item from a specific slot
        Returns True if successful, False otherwise
        """
        try:
            if slot not in self.equipment:
                MessageView.show_error(f"Invalid slot: {slot}")
                return False

            if self.equipment[slot]:
                old_item = self.equipment[slot]
                for stat, value in old_item.stat_modifiers.items():
                    current = getattr(self, stat, 0)
                    setattr(self, stat, current - value)
                self.inventory["items"].append(old_item)

            self.equipment[slot] = None
            MessageView.show_success(f"Unequipped item from {slot}")
            return True

        except Exception as e:
            MessageView.show_error(f"Failed to unequip item from {slot}: {str(e)}")
            return False

    def get_total_attack(self) -> int:
        """Calculate total attack including equipment bonuses"""
        total = self.attack
        for equipment in self.equipment.values():
            if equipment and isinstance(equipment.stat_modifiers, dict):
                for stat, value in equipment.stat_modifiers.items():
                    if stat == "attack":
                        total += value
        return total

    def get_total_defense(self) -> int:
        """Calculate total defense including equipment bonuses"""
        total = self.defense
        for equipment in self.equipment.values():
            if equipment and isinstance(equipment.stat_modifiers, dict):
                for stat, value in equipment.stat_modifiers.items():
                    if stat == "defense":
                        total += value
        return total

    def rest(self) -> int:
        """Rest to recover health and mana
        Returns the amount of health recovered"""
        max_heal = self.max_health - self.health
        heal_amount = min(
            max_heal, int(self.max_health * 0.3)
        )  # Heal 30% of max health

        self.health = min(self.max_health, self.health + heal_amount)
        self.mana = min(
            self.max_mana, self.mana + int(self.max_mana * 0.3)
        )  # Recover 30% of max mana

        return heal_amount

    def serialize(self) -> Dict[str, Any]:
        """Serialize player data to a dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "exp": self.exp,
            "exp_to_level": self.exp_to_level,
            "inventory": self.inventory,
            "equipment": {
                slot: item.serialize() if item else None
                for slot, item in self.equipment.items()
            },
            "skills": [skill.serialize() for skill in self.skills],
            "session_id": self.session_id,
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "Player":
        """Deserialize player data from a dictionary"""
        char_class = CharacterClass(
            name=data["char_class"]["name"],
            description=data["char_class"]["description"],
            base_health=data["char_class"]["base_health"],
            base_mana=data["char_class"]["base_mana"],
            base_attack=data["char_class"]["base_attack"],
            base_defense=data["char_class"]["base_defense"],
            skills=[Skill.deserialize(skill) for skill in data["char_class"]["skills"]],
        )
        player = cls(name=data["name"], char_class=char_class)
        player.description = data["description"]
        player.health = data["health"]
        player.max_health = data["max_health"]
        player.attack = data["attack"]
        player.defense = data["defense"]
        player.level = data["level"]
        player.mana = data["mana"]
        player.max_mana = data["max_mana"]
        player.exp = data["exp"]
        player.exp_to_level = data["exp_to_level"]
        player.inventory = data["inventory"]
        player.equipment = {
            slot: Equipment.deserialize(item) if item else None
            for slot, item in data["equipment"].items()
        }
        player.skills = [Skill.deserialize(skill) for skill in data["skills"]]
        player.session_id = data["session_id"]
        return player

class Enemy(Character):
    def __init__(
        self,
        name: str,
        description: str,
        health: int,
        attack: int,
        defense: int,
        exp_reward: int,
        level: int,
        art: str = None,
    ):
        super().__init__(name, description, health, attack, defense, level)
        self.exp_reward = exp_reward
        self.art = art
        self.max_health = health

    def get_drops(self) -> List["Item"]:  # type: ignore
        """Calculate and return item drops"""
        # Implementation for item drops can be added here
        return []

    def get_exp_reward(self) -> int:
        """Return the experience reward for defeating this enemy"""
        return self.exp_reward

    def serialize(self) -> Dict[str, Any]:
        """Serialize enemy data to a dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "exp_reward": self.exp_reward,
            "art": self.art,
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "Enemy":
        """Deserialize enemy data from a dictionary"""
        return cls(
            name=data["name"],
            description=data["description"],
            health=data["health"],
            attack=data["attack"],
            defense=data["defense"],
            exp_reward=data["exp_reward"],
            level=data["level"],
            art=data.get("art"),
        )


def get_fallback_enemy(player_level: int = 1) -> Enemy:
    """Create a fallback enemy when generation fails"""
    fallback_enemies = [
        {
            "name": "Shadow Wraith",
            "description": "A dark spirit that haunts the shadows",
            "base_health": 50,
            "level": 1,
            "base_attack": 10,
            "base_defense": 3,
            "exp_reward": 20,
            "art": """
     ╔═══════╗
     ║ ◇◇◇◇◇ ║
     ║ ▓▓▓▓▓ ║
     ║ ░░░░░ ║
     ╚═══════╝
            """,
        },
        {
            "name": "Corrupted Zealot",
            "description": "A fallen warrior consumed by darkness",
            "base_health": 60,
            "base_attack": 12,
            "level": 1,
            "base_defense": 4,
            "exp_reward": 20,
            "art": """
     ╔═══════╗
     ║ ▲▲▲▲▲ ║
     ║ ║║║║║ ║
     ║ ▼▼▼▼▼ ║
     ╚═══════╝
            """,
        },
        {
            "name": "Ghastly Apparition",
            "description": "A spectral figure roaming through the night, seeking vengeance",
            "base_health": 70,
            "level": 2,
            "base_attack": 14,
            "base_defense": 5,
            "exp_reward": 30,
            "art": """
     ╔═══════╗
     ║ ☽☽☽☽☽ ║
     ║ ☾☾☾☾☾ ║
     ║ ☽☽☽☽☽ ║
     ╚═══════╝
            """,
        },
        {
            "name": "Doomed Knight",
            "description": "A once noble knight, now twisted by dark magic and bound to eternal servitude",
            "base_health": 80,
            "level": 3,
            "base_attack": 16,
            "base_defense": 6,
            "exp_reward": 40,
            "art": """
     ╔═══════╗
     ║ ⚔⚔⚔⚔⚔ ║
     ║ ⚔⚔⚔⚔⚔ ║
     ║ ⚔⚔⚔⚔⚔ ║
     ╚═══════╝
            """,
        },
        {
            "name": "Ancient Lich",
            "description": "An age-old sorcerer who has transcended death to wield necromantic powers",
            "base_health": 90,
            "level": 4,
            "base_attack": 18,
            "base_defense": 7,
            "exp_reward": 50,
            "art": """
     ╔═══════╗
     ║ ✵✵✵✵✵ ║
     ║ ✵✵✵✵✵ ║
     ║ ✵✵✵✵✵ ║
     ╚═══════╝
            """,
        },
        {
            "name": "Harbinger of Despair",
            "description": "A creature born from the deepest fears of mankind, it brings nothing but despair",
            "base_health": 100,
            "level": 5,
            "base_attack": 20,
            "base_defense": 8,
            "exp_reward": 60,
            "art": """
     ╔═══════╗
     ║ ░░░░░░ ║
     ║ ░░░░░░ ║
     ║ ░░░░░░ ║
     ╚═══════╝
            """,
        },
    ]

    enemy_data = random.choice(fallback_enemies)

    return Enemy(
        name=enemy_data["name"],
        description=enemy_data["description"],
        health=enemy_data["base_health"],
        attack=enemy_data["base_attack"],
        defense=enemy_data["base_defense"],
        level=enemy_data["level"],
        art=enemy_data["art"],
        exp_reward=enemy_data["exp_reward"],
    )
