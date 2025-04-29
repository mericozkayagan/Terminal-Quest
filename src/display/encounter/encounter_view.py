from typing import Dict, Any, List
from src.display.base.base_view import BaseView
from src.display.themes.dark_theme import DECORATIONS as dec
from src.display.themes.dark_theme import SYMBOLS as sym
from src.models.base_types import EncounterType
from src.models.character import Player
import time
import random


class EncounterView(BaseView):
    """View for displaying different types of encounters"""

    @staticmethod
    def show_encounter(encounter_data: Dict[str, Any]):
        """Show encounter based on type"""
        BaseView.clear_screen()
        encounter_type = encounter_data.get("type")

        print(f"\n{dec['TITLE']['PREFIX']}Encounter{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        if encounter_type == EncounterType.PUZZLE:
            EncounterView.show_puzzle_encounter(encounter_data)
        elif encounter_type == EncounterType.TREASURE:
            EncounterView.show_treasure_encounter(encounter_data)
        elif encounter_type == EncounterType.TRAP:
            EncounterView.show_trap_encounter(encounter_data)
        elif encounter_type == EncounterType.NPC:
            EncounterView.show_npc_encounter(encounter_data)

    @staticmethod
    def show_puzzle_encounter(puzzle_data: Dict[str, Any]):
        """Display puzzle encounter"""
        print(f"\n{dec['SECTION']['START']}Puzzle{dec['SECTION']['END']}")
        print(f"\n{puzzle_data['scene']}")

        print(f"\n{sym['PUZZLE']} {puzzle_data['puzzle']}")
        print(f"\n{dec['SECTION']['START']}Options{dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} 1. Solve the puzzle")
        print(f"  {sym['CURSOR']} 2. Request a hint")
        print(f"  {sym['CURSOR']} 3. Skip the puzzle")

    @staticmethod
    def show_hint(hint: str):
        """Display a hint for the puzzle"""
        print(f"\n{sym['HINT']} Hint: {hint}")

    @staticmethod
    def show_puzzle_success(reward: Dict[str, Any]):
        """Display successful puzzle completion"""
        print(f"\n{dec['SECTION']['START']}Success!{dec['SECTION']['END']}")
        print(f"\n{sym['SUCCESS']} You solved the puzzle!")

        reward_type = reward.get("type", "gold")
        amount = reward.get("amount", 10)

        if reward_type == "gold":
            print(f"\n{sym['GOLD']} Reward: {amount} gold")
        elif reward_type == "health":
            print(f"\n{sym['HEALTH']} Reward: {amount} health restored")
        elif reward_type == "mana":
            print(f"\n{sym['MANA']} Reward: {amount} mana restored")
        elif reward_type == "exp":
            print(f"\n{sym['EXP']} Reward: {amount} experience")

        print("\nPress Enter to continue...")

    @staticmethod
    def show_puzzle_failure():
        """Display puzzle failure"""
        print(f"\n{dec['SECTION']['START']}Failure{dec['SECTION']['END']}")
        print(f"\n{sym['FAILURE']} You failed to solve the puzzle.")
        print("\nPress Enter to continue...")

    @staticmethod
    def show_treasure_encounter(treasure_data: Dict[str, Any]):
        """Display treasure encounter"""
        print(f"\n{dec['SECTION']['START']}Treasure{dec['SECTION']['END']}")
        print(f"\n{treasure_data['description']}")

        gold = treasure_data.get("gold", 0)
        has_item = treasure_data.get("has_item", False)

        # Visual treasure display
        print("\n  ╔═════════╗")
        print("  ║ ╭─────╮ ║")
        print("  ║ │ $$$ │ ║")
        print("  ║ ╰─────╯ ║")
        print("  ╚═════════╝")

        print(f"\n{sym['GOLD']} You found {gold} gold coins!")

        if has_item:
            print(f"{sym['ITEM']} There's an item inside the treasure chest!")

        print("\nPress Enter to continue...")

    @staticmethod
    def show_trap_encounter(trap_data: Dict[str, Any]):
        """Display trap encounter"""
        print(f"\n{dec['SECTION']['START']}Trap{dec['SECTION']['END']}")
        print(f"\n{trap_data['description']}")

        print(f"\n{dec['SECTION']['START']}Options{dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} 1. Try to disarm the trap")
        print(f"  {sym['CURSOR']} 2. Attempt to avoid the trap")
        print(f"  {sym['CURSOR']} 3. Accept the consequences and move on")

    @staticmethod
    def show_trap_result(success: bool, trap_data: Dict[str, Any]):
        """Display trap result"""
        if success:
            print(f"\n{sym['SUCCESS']} {trap_data['evaded_text']}")
            print("\nPress Enter to continue...")
        else:
            print(f"\n{sym['FAILURE']} {trap_data['triggered_text']}")
            damage = trap_data.get("damage", 5)
            print(f"{sym['DAMAGE']} You take {damage} damage!")
            print("\nPress Enter to continue...")

    @staticmethod
    def show_npc_encounter(npc_data: Dict[str, Any]):
        """Display NPC encounter"""
        print(f"\n{dec['SECTION']['START']}NPC Encounter{dec['SECTION']['END']}")

        npc_name = npc_data.get("npc_name", "Stranger")
        description = npc_data.get("description", "")
        dialogue = npc_data.get("dialogue", "...")

        print(f"\n{sym['NPC']} {npc_name}")
        print(f"\n{description}")

        # ASCII art of NPC (generic)
        print("\n      ╭─────╮")
        print("      │ o_o │")
        print("      │  ┼  │")
        print("      ╰─────╯")

        # NPC dialogue
        print(f'\n"{dialogue}"')

        # Show response options
        print(f"\n{dec['SECTION']['START']}Your Response{dec['SECTION']['END']}")
        options = npc_data.get("options", [])
        for i, option in enumerate(options, 1):
            print(f"  {sym['CURSOR']} {i}. {option['text']}")

    @staticmethod
    def show_npc_outcome(outcome: str):
        """Display outcome of NPC interaction"""
        print(f"\n{dec['SECTION']['START']}Outcome{dec['SECTION']['END']}")
        print(f"\n{outcome}")
        print("\nPress Enter to continue...")

    @staticmethod
    def show_encounter_transition():
        """Show transition between encounters"""
        transitions = [
            "The shadows shift around you...",
            "You continue your journey through the corrupted realm...",
            "The air grows thick with twisted energy...",
            "A whisper of false hope lingers in the air...",
            "The path ahead grows darker...",
        ]

        print(f"\n{random.choice(transitions)}")
        time.sleep(1.5)
