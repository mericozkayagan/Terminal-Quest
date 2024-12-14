from typing import List, Optional
from src.config.settings import DISPLAY_SETTINGS
from src.models.items.consumable import Consumable
from src.display.base.base_view import BaseView
from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.themes.dark_theme import DECORATIONS as dec
from src.models.character import Player, Enemy, Character
import random
import time
from src.models.effects.base import BaseEffect
from src.models.base_types import EffectTrigger


class CombatView(BaseView):
    """Handles all combat-related display logic"""

    @staticmethod
    def show_combat_status(
        players: List[Player], enemies: List[Enemy], combat_log: List[str]
    ):
        """Display combat status with improved visual flow"""
        print(f"\n{dec['TITLE']['PREFIX']}Combat{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        # Enemy section
        print(f"\n{dec['SECTION']['START']}Enemies{dec['SECTION']['END']}")
        for enemy in enemies:
            print(f"  {sym['SKULL']} {enemy.name}\n")

            # Show enemy art if available
            if hasattr(enemy, "art") and enemy.art:
                print(enemy.art)
            else:
                # Display default art or placeholder
                print("     ╔════════╗")
                print("     ║  (??)  ║")
                print("     ║  (||)  ║")
                print("     ╚════════╝")

            # Enemy health bar
            health_percent = enemy.health / enemy.max_health
            health_bar = "█" * int(health_percent * 20)
            health_bar = health_bar.ljust(20, "░")
            print(f"\n  {sym['HEALTH']} Health: {enemy.health}/{enemy.max_health}")
            print(f"  [{health_bar}]")

        # Combat log section
        if combat_log:
            print(f"\n{dec['SECTION']['START']}Combat Log{dec['SECTION']['END']}")
            for message in combat_log[:5]:  # Show only last 5 messages
                print(f"  {message}")

        # Player status
        print(f"\n{dec['SECTION']['START']}Players{dec['SECTION']['END']}")
        for player in players:
            # Player health bar
            player_health_percent = player.health / player.max_health
            player_health_bar = "█" * int(player_health_percent * 20)
            player_health_bar = player_health_bar.ljust(20, "░")
            print(f"  {sym['HEALTH']} Health: {player.health}/{player.max_health}")
            print(f"  [{player_health_bar}]")

            # Player mana bar
            mana_percent = player.mana / player.max_mana
            mana_bar = "█" * int(mana_percent * 20)
            mana_bar = mana_bar.ljust(20, "░")
            print(f"  {sym['MANA']} Mana:   {player.mana}/{player.max_mana}")
            print(f"  [{mana_bar}]")

        # Actions
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
            status = (
                "Ready"
                if skill.is_available()
                else f"Cooldown: {skill.current_cooldown}"
            )
            print(f"\n  {rune} {i}. {skill.name} [{status}]")
            print(f"    {sym['ATTACK']} Power: {skill.damage}")
            print(f"    {sym['MANA']} Cost: {skill.mana_cost}")
            print(f"    {sym['RUNE']} {skill.description}")

    @staticmethod
    def show_battle_result(player: Player, enemy: Enemy, rewards: dict):
        """Display battle results with a simple dark RPG theme"""
        print(f"\n{dec['TITLE']['PREFIX']}Battle Results{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        print("\n  The enemy is defeated.")
        print(f"  {sym['SKULL']} {enemy.name} has fallen.")

        print(f"\n{dec['SECTION']['START']}Rewards{dec['SECTION']['END']}")
        print(f"  {sym['EXP']} Experience: +{rewards.get('exp', 0)}")
        print(f"  {sym['GOLD']} Gold: +{rewards.get('gold', 0)}")

        if rewards.get("items"):
            print(f"\n{dec['SECTION']['START']}Items Collected{dec['SECTION']['END']}")
            for item in rewards["items"]:
                rune = random.choice(dec["RUNES"])
                print(f"  {rune} {item.name} ({item.rarity.value})")

        time.sleep(2)

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
        time.sleep(2)

    @staticmethod
    def show_status_effect(character: Character, effect_name: str, damage: int = 0):
        """Display status effect information"""
        print(f"\n{dec['SECTION']['START']}Status Effect{dec['SECTION']['END']}")
        print(f"  {character.name} is affected by {effect_name}")
        if damage:
            print(f"  {effect_name} deals {damage} damage")

    @staticmethod
    def show_combat_items(player: Player):
        """Display usable items during combat"""
        print(f"\n{dec['TITLE']['PREFIX']}Combat Items{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        # Filter for consumable items
        usable_items = [
            (i, item)
            for i, item in enumerate(player.inventory["items"], 1)
            if isinstance(item, Consumable)
        ]

        if usable_items:
            for i, (_, item) in enumerate(usable_items, 1):
                rune = random.choice(dec["RUNES"])
                print(f"\n  {rune} [{i}] {item.name}")
                if hasattr(item, "healing") and item.healing > 0:
                    print(f"    {sym['HEALTH']} Healing: {item.healing}")
                if hasattr(item, "mana_restore") and item.mana_restore > 0:
                    print(f"    {sym['MANA']} Mana: {item.mana_restore}")
                print(f"    ✧ Rarity: {item.rarity.value}")
        else:
            print("\n  No usable items available...")

        print(f"\n{dec['SECTION']['START']}Actions{dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} Enter item number to use")
        print(f"  {sym['CURSOR']} 0 to return")

    @staticmethod
    def show_retreat_attempt(
        success: bool, damage_taken: int = 0, enemy_name: str = ""
    ):
        """Display retreat attempt result"""
        print(f"\n{dec['TITLE']['PREFIX']}Retreat Attempt{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        if success:
            print(f"\n  {sym['RUNE']} You successfully escape from battle...")
            print(f"  {sym['RUNE']} The shadows conceal your retreat")
        else:
            print(f"\n  {sym['SKULL']} Failed to escape!")
            print(f"  {sym['ATTACK']} {enemy_name} strikes you as you flee")
            print(f"  {sym['HEALTH']} You take {damage_taken} damage")

        time.sleep(2)  # Give time to read the message

    @staticmethod
    def show_effect_trigger(
        effect: BaseEffect, source: "Character", target: Optional["Character"] = None
    ):
        """Display effect activation during combat"""
        effect_symbol = {
            EffectTrigger.ON_HIT: sym["ATTACK"],
            EffectTrigger.ON_HIT_TAKEN: sym["DEFENSE"],
            EffectTrigger.ON_TURN_START: sym["TIME"],
            EffectTrigger.ON_TURN_END: sym["TIME"],
            EffectTrigger.ON_KILL: sym["SKULL"],
            EffectTrigger.PASSIVE: sym["BUFF"],
        }.get(effect.trigger, sym["EFFECT"])

        message = f"{effect_symbol} {source.name}'s {effect.name} activates!"
        if target:
            message += f" on {target.name}"

        print(message)
        time.sleep(DISPLAY_SETTINGS["COMBAT_MESSAGE_DELAY"])
