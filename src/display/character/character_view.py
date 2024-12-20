from typing import List
import random

from src.models.character_classes import CharacterClass
from src.display.base.base_view import BaseView
from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.themes.dark_theme import DECORATIONS as dec


class CharacterView(BaseView):
    """Handles all character-related display logic"""

    @staticmethod
    def show_character_creation():
        """Display character creation screen"""
        BaseView.clear_screen()
        print(f"\n{dec['TITLE']['PREFIX']}Dark Genesis{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")
        print("\nSpeak thy name, dark one:")
        print(f"{dec['SMALL_SEP']}")

    @staticmethod
    def show_character_class(char_class: "CharacterClass"):
        """Display character class details"""
        BaseView.clear_screen()
        print(f"\n{dec['TITLE']['PREFIX']}{char_class.name}{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        if hasattr(char_class, "art") and char_class.art:
            print(f"\n{char_class.art}")

        CharacterView._show_stats(char_class)
        CharacterView._show_description(char_class)
        CharacterView._show_skills(char_class)

    @staticmethod
    def show_class_selection(classes: List["CharacterClass"]):
        """Display class selection screen"""
        try:
            print(
                f"\n{dec['TITLE']['PREFIX']}Choose Your Dark Path{dec['TITLE']['SUFFIX']}"
            )
            print(f"{dec['SEPARATOR']}")

            for i, char_class in enumerate(classes, 1):
                # Add separator between classes
                if i > 1:
                    print("\n" + "─" * 40 + "\n")

                print(
                    f"\n{dec['SECTION']['START']}{i}. {char_class.name}{dec['SECTION']['END']}"
                )

                if char_class.art:
                    print(f"\n{char_class.art}")
                else:
                    print("\n[No art available]")

                print(f"\n  {char_class.description}")
                print(f"\n{dec['SMALL_SEP']}")
                print(f"  {sym['HEALTH']} Health    {char_class.base_health}")
                print(f"  {sym['MANA']} Mana      {char_class.base_mana}")
                print(f"  {sym['ATTACK']} Attack    {char_class.base_attack}")
                print(f"  {sym['DEFENSE']} Defense   {char_class.base_defense}")

                if char_class.skills:
                    print(f"\n  ✤ Skills:")
                    for skill in char_class.skills:
                        rune = random.choice(dec["RUNES"])
                        print(f"    {rune} {skill.name}")
                        print(f"      {sym['ATTACK']} Power: {skill.damage}")
                        print(f"      {sym['MANA']} Cost: {skill.mana_cost}")
                        print(f"      {sym['COOLDOWN']} Cooldown: {skill.cooldown}")
                        print(
                            f"      {random.choice(dec['RUNES'])} {skill.description}"
                        )

        except Exception as e:
            print("\n⚠ Error ⚠")
            print(f"  An error occurred: {str(e)}")

    @staticmethod
    def _show_stats(char_class: "CharacterClass"):
        """Display character stats"""
        print(f"\n{dec['SECTION']['START']}Base Stats{dec['SECTION']['END']}")
        print(f"  {sym['HEALTH']} Health    {char_class.base_health}")
        print(f"  {sym['MANA']} Mana      {char_class.base_mana}")
        print(f"  {sym['ATTACK']} Attack    {char_class.base_attack}")
        print(f"  {sym['DEFENSE']} Defense   {char_class.base_defense}")

    @staticmethod
    def _show_description(char_class: "CharacterClass"):
        """Display character description"""
        print(f"\n{dec['SECTION']['START']}Dark Path{dec['SECTION']['END']}")
        print(f"  {char_class.description}")

    @staticmethod
    def _show_skills(char_class: "CharacterClass"):
        """Display character skills"""
        print(f"\n{dec['SECTION']['START']}Innate Arts{dec['SECTION']['END']}")
        for skill in char_class.skills:
            rune = random.choice(dec["RUNES"])
            print(f"\n  {rune} {skill.name}")
            print(f"    {sym['ATTACK']} Power: {skill.damage}")
            print(f"    {sym['MANA']} Cost: {skill.mana_cost}")
            print(f"    {sym['RUNE']} {skill.description}")
            print(f"    {sym['COOLDOWN']} Cooldown: {skill.cooldown}")
