from typing import List
from src.display.base.base_view import BaseView
from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.themes.dark_theme import DECORATIONS as dec
from src.models.character import Player, Enemy, Character
import random


class CombatView(BaseView):
    """Handles all combat-related display logic"""

    @staticmethod
    def show_combat_status(player: Player, enemy: Enemy):
        """Display combat status"""
        print(f"\n{dec['TITLE']['PREFIX']}Combat{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        # Enemy details
        print(f"\n{dec['SECTION']['START']}Enemy{dec['SECTION']['END']}")
        print(f"  {sym['SKULL']} {enemy.name}")
        print(f"  {sym['HEALTH']} Health: {enemy.health}")

        # Player status
        print(f"\n{dec['SECTION']['START']}Status{dec['SECTION']['END']}")
        print(f"  {sym['HEALTH']} Health: {player.health}/{player.max_health}")
        print(f"  {sym['MANA']} Mana:   {player.mana}/{player.max_mana}")

        # Combat actions
        print(f"\n{dec['SECTION']['START']}Actions{dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} 1. Attack")
        print(f"  {sym['CURSOR']} 2. Use Skill")
        print(f"  {sym['CURSOR']} 3. Use Item")
        print(f"  {sym['CURSOR']} 4. Run")

    @staticmethod
    def show_skills(player: Player):
        """Display available skills"""
        print(f"\n{dec['TITLE']['PREFIX']}Dark Arts{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        for i, skill in enumerate(player.skills, 1):
            rune = random.choice(dec["RUNES"])
            print(f"\n  {rune} {i}. {skill.name}")
            print(f"    {sym['ATTACK']} Power: {skill.damage}")
            print(f"    {sym['MANA']} Cost: {skill.mana_cost}")
            print(f"    {sym['RUNE']} {skill.description}")

    @staticmethod
    def show_battle_result(player: Player, enemy: Enemy, rewards: dict):
        """Display battle results with dark theme"""
        print(f"\n{dec['TITLE']['PREFIX']}Battle Aftermath{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        print("\n  The enemy's essence fades...")
        print(f"  {sym['SKULL']} {enemy.name} has fallen")

        print(f"\n{dec['SECTION']['START']}Dark Rewards{dec['SECTION']['END']}")
        print(f"  {sym['EXP']} Soul Essence: +{rewards.get('exp', 0)}")
        print(f"  {sym['GOLD']} Dark Tokens: +{rewards.get('gold', 0)}")

        if rewards.get("items"):
            print(
                f"\n{dec['SECTION']['START']}Claimed Artifacts{dec['SECTION']['END']}"
            )
            for item in rewards["items"]:
                rune = random.choice(dec["RUNES"])
                print(f"  {rune} {item.name} ({item.rarity.value})")

    @staticmethod
    def show_level_up(player: Player):
        """Display level up information"""
        print(f"\n{dec['TITLE']['PREFIX']}Dark Ascension{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")
        print(f"\nYou have reached level {player.level}!")
        print("\nYour powers grow stronger:")
        print(f"  {sym['HEALTH']} Health increased")
        print(f"  {sym['MANA']} Mana increased")
        print(f"  {sym['ATTACK']} Attack improved")
        print(f"  {sym['DEFENSE']} Defense improved")

    @staticmethod
    def show_status_effect(character: Character, effect_name: str, damage: int = 0):
        """Display status effect information"""
        print(f"\n{dec['SECTION']['START']}Status Effect{dec['SECTION']['END']}")
        print(f"  {character.name} is affected by {effect_name}")
        if damage:
            print(f"  {effect_name} deals {damage} damage")
