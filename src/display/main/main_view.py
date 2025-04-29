from typing import Dict, List
from src.display.base.base_view import BaseView
from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.themes.dark_theme import DECORATIONS as dec
from src.models.character import Player
import random
from src.services.encounter import EncounterService


class GameView(BaseView):
    """Handles main game display logic"""

    @staticmethod
    def show_main_status(character: Player):
        """Display main game status"""
        print(
            f"\n{dec['TITLE']['PREFIX']}{character.name} | {character.char_class.name}{dec['TITLE']['SUFFIX']}"
        )
        print(f"{dec['SEPARATOR']}")

        # Core attributes
        print(f"\n{dec['SECTION']['START']}Stats{dec['SECTION']['END']}")
        print(f"  {sym['HEALTH']} Health    {character.health}/{character.max_health}")
        print(f"  {sym['MANA']} Mana      {character.mana}/{character.max_mana}")
        print(f"  {sym['ATTACK']} Attack    {character.get_total_attack()}")
        print(f"  {sym['DEFENSE']} Defense   {character.get_total_defense()}")

        # Progress
        print(f"\n{dec['SECTION']['START']}Progress{dec['SECTION']['END']}")
        print(f"  {sym['EXP']} Level     {character.level}")
        print(f"  {sym['EXP']} Exp       {character.exp}/{character.exp_to_level}")
        print(f"  {sym['GOLD']} Gold      {character.inventory['Gold']}")

        # Get boss progress from the CURRENT singleton instance
        encounter_service = EncounterService()  # Get the singleton instance dynamically
        boss_progress = encounter_service.get_boss_progress()

        # Display boss progress
        if boss_progress:
            total = boss_progress["total_boss_interval"]
            remaining = boss_progress["encounters_until_boss"]
            completed = total - remaining

            # Use symbols from dark theme for progress: completed encounters, remaining, and boss
            # Add spacing between symbols for better readability
            progress_symbols = (
                f"{sym['SUCCESS']} " * completed
                + f"{sym['TAINT']} " * remaining
                + f"{sym['SKULL']}"
            )

            print(f"\n{dec['SECTION']['START']}Corruption Path{dec['SECTION']['END']}")
            print(f"  {sym['SKULL']} Boss Path: {progress_symbols}")

            # Show numeric progress with different descriptions based on progress percentage
            progress_percent = ((total - remaining) / total) * 100
            if remaining <= 0:
                print(
                    f"  {sym['WARNING']} The corruption has manifested! Prepare for battle!"
                )
            elif progress_percent >= 75:
                print(
                    f"  {sym['WARNING']} The corruption grows strong... {remaining} encounters remain."
                )
            elif progress_percent >= 50:
                print(
                    f"  {sym['INFO']} The corruption gathers... {remaining} encounters until manifestation."
                )
            elif progress_percent >= 25:
                print(
                    f"  {sym['INFO']} Corruption stirs in the distance... {remaining} encounters until manifestation."
                )
            else:
                print(
                    f"  {sym['INFO']} {remaining} encounters until the corruption manifests..."
                )

        # Equipment
        if any(character.equipment.values()):
            print(f"\n{dec['SECTION']['START']}Equipment{dec['SECTION']['END']}")
            for slot, item in character.equipment.items():
                if item:
                    rune = random.choice(dec["RUNES"])
                    print(f"  {rune} {slot.title():<10} {item.name}")

        # Actions
        print(f"\n{dec['SECTION']['START']}Actions{dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} 1  Explore")
        print(f"  {sym['CURSOR']} 2  Shop")
        print(f"  {sym['CURSOR']} 3  Rest")
        print(f"  {sym['CURSOR']} 4  Inventory")
        print(f"  {sym['CURSOR']} 5  Exit")

        # Check if boss is ready and add option if so
        # Re-fetch the instance here too for consistency, although boss_progress already has the data
        encounter_service = EncounterService()  # Get the singleton instance dynamically
        boss_progress = (
            encounter_service.get_boss_progress()
        )  # Or reuse the boss_progress dict from above
        if boss_progress and boss_progress["encounters_until_boss"] <= 0:
            print(f"  {sym['CURSOR']} 6  Face the Corruption {sym['SKULL']}")

        # Themed input prompt
        print(f"\n{dec['SMALL_SEP']}")
        print(f"{sym['RUNE']} Choose your path, dark one: ", end="")

    @staticmethod
    def show_dark_fate(player: Player):
        """Display game over screen"""
        print(
            f"\n{dec['TITLE']['PREFIX']} {sym['SKULL']} Dark Fate {sym['SKULL']} {dec['TITLE']['SUFFIX']}"
        )
        print(f"{dec['SEPARATOR']}")

        print("\nYour soul has been consumed...")
        print(f"\n{sym['MANA']} Final Level: {player.level}")
        print(f"{sym['GOLD']} Gold Amassed: {player.inventory['Gold']}")
        print("\nThe darkness claims another...")

    @staticmethod
    def show_sell_inventory(player: Player, sell_multiplier: float):
        """Display player's sellable inventory"""
        print("\n╔════════════ ◈ Your Treasures ◈ ════════════╗")
        if not player.inventory["items"]:
            print("║          Your satchel is empty...          ║")
            print("╚══════════════════════════════════════════════╝")
            return

        for i, item in enumerate(player.inventory["items"], 1):
            try:
                sell_value = max(1, int(item.value * sell_multiplier))
            except (OverflowError, ValueError):
                sell_value = 1
            print(f"║ {i}. {item.name:<28} │ ◈ {sell_value} Gold ║")
        print("╚══════════════════════════════════════════════╝")
        print("\nChoose an item to sell (0 to cancel): ")

    @staticmethod
    def show_inventory(player: Player):
        """Display inventory with dark theme"""
        print(f"\n{dec['TITLE']['PREFIX']}Inventory{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        # Equipment section
        print(f"\n{dec['SECTION']['START']}Bound Artifacts{dec['SECTION']['END']}")
        for slot, item in player.equipment.items():
            rune = random.choice(dec["RUNES"])
            name = item.name if item else "None"
            print(f"  {rune} {slot.title():<10} {name}")

        # Items section
        print(f"\n{dec['SECTION']['START']}Possessed Items{dec['SECTION']['END']}")
        if player.inventory["items"]:
            for i, item in enumerate(player.inventory["items"], 1):
                rune = random.choice(dec["RUNES"])
                print(f"\n  {rune} {item.name}")
                if hasattr(item, "stat_modifiers"):
                    mods = [
                        f"{stat}: {value}"
                        for stat, value in item.stat_modifiers.items()
                    ]
                    print(f"    {sym['ATTACK']} Power: {', '.join(mods)}")
                if hasattr(item, "durability"):
                    print(
                        f"    {sym['EQUIPMENT']} Durability: {item.durability}/{item.max_durability}"
                    )
                print(f"    ✧ Rarity: {item.rarity.value}")
        else:
            print("  Your collection is empty...")

    @staticmethod
    def show_game_over(player: Player):
        """Display game over screen"""
        print(
            f"\n{dec['TITLE']['PREFIX']} {sym['SKULL']} Dark Fate {sym['SKULL']} {dec['TITLE']['SUFFIX']}"
        )
        print(f"{dec['SEPARATOR']}")

        print("\nYour soul has been consumed by darkness...")
        print(f"\n{sym['MANA']} Final Level: {player.level}")
        print(f"{sym['GOLD']} Gold Amassed: {player.inventory['Gold']}")
        print(f"{sym['EXP']} Experience Gained: {player.exp}")
        print("\nThe darkness claims another wanderer...")
