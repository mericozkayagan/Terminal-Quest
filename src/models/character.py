from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random
from .character_classes import CharacterClass
from .status_effects import StatusEffect


class Character:
    def __init__(self):
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
        super().__init__()
        self.name = name
        self.char_class = char_class
        self.health = char_class.base_health
        self.max_health = char_class.base_health
        self.attack = char_class.base_attack
        self.defense = char_class.base_defense
        self.mana = char_class.base_mana
        self.max_mana = char_class.base_mana
        self.inventory = {"Health Potion": 2, "Mana Potion": 2, "Gold": 0, "items": []}
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.skills = char_class.skills

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


class Enemy(Character):
    def __init__(
        self, name: str, health: int, attack: int, defense: int, exp: int, gold: int
    ):
        super().__init__()
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.gold = gold


def get_fallback_enemy() -> Enemy:
    """Return a random fallback enemy when AI generation fails"""
    enemies = [
        Enemy("Goblin", 30, 8, 2, 20, 10),
        Enemy("Skeleton", 45, 12, 4, 35, 20),
        Enemy("Orc", 60, 15, 6, 50, 30),
        Enemy("Dark Mage", 40, 20, 3, 45, 25),
        Enemy("Dragon", 100, 25, 10, 100, 75),
    ]
    return random.choice(enemies)
