from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random
from .character_classes import CharacterClass
from .status_effects import StatusEffect
from ..utils.ascii_art import ensure_entity_art


class Character:
    def __init__(
        self,
        name: str,
        description: str = "",
        health: int = 100,
        attack: int = 15,
        defense: int = 5,
        level: int = 1,
    ):
        # Basic attributes
        self.name = name
        self.description = description
        self.level = level

        # Combat stats
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense

        # Status and equipment
        self.status_effects: Dict[str, StatusEffect] = {}
        self.equipment: Dict[str, Optional["Equipment"]] = {  # type: ignore
            "weapon": None,
            "armor": None,
            "accessory": None,
        }

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
            if equipment and "attack" in equipment.stat_modifiers:
                total += equipment.stat_modifiers["attack"]
        return total

    def get_total_defense(self) -> int:
        """Calculate total defense including equipment bonuses"""
        total = self.defense
        for equipment in self.equipment.values():
            if equipment and "defense" in equipment.stat_modifiers:
                total += equipment.stat_modifiers["defense"]
        return total


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

        # Inventory
        self.inventory = {"Health Potion": 2, "Mana Potion": 2, "Gold": 0, "items": []}

    def equip_item(self, item: "Equipment", slot: str) -> Optional["Equipment"]:  # type: ignore
        """Equip an item and return the previously equipped item if any"""
        if slot not in self.equipment:
            return None

        old_item = self.equipment[slot]
        if old_item:
            old_item.unequip(self)

        self.equipment[slot] = item
        item.equip(self)
        return old_item

    def rest(self) -> int:
        """Rest to recover health and mana
        Returns the amount of health recovered"""
        max_heal = self.max_health - self.health
        heal_amount = min(max_heal, self.max_health * 0.3)  # Heal 30% of max health

        self.health = min(self.max_health, self.health + heal_amount)
        self.mana = min(
            self.max_mana, self.mana + self.max_mana * 0.3
        )  # Recover 30% of max mana

        return int(heal_amount)


class Enemy(Character):
    def __init__(
        self,
        name: str,
        description: str,
        health: int,
        attack: int,
        defense: int,
        level: int = 1,
        art: str = None,
    ):
        super().__init__(name, description, health, attack, defense, level)
        self.art = art
        self.max_health = health
        self.exp_reward = level * 10  # Simple exp reward based on level

    def get_drops(self) -> List["Item"]:  # type: ignore
        """Calculate and return item drops"""
        # Implementation for item drops can be added here
        return []


def get_fallback_enemy(player_level: int = 1) -> Enemy:
    """Create a fallback enemy when generation fails"""
    fallback_enemies = [
        {
            "name": "Shadow Wraith",
            "description": "A dark spirit that haunts the shadows",
            "base_health": 50,
            "base_attack": 10,
            "base_defense": 3,
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
            "base_defense": 4,
            "art": """
     ╔═══════╗
     ║ ▲▲▲▲▲ ║
     ║ ║║║║║ ║
     ║ ▼▼▼▼▼ ║
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
        level=player_level,
        art=enemy_data["art"],
        exp_reward=player_level * 10,
    )
