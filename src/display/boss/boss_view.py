from typing import Optional
from ..base.base_view import BaseView
from ..themes.dark_theme import DECORATIONS as dec, SYMBOLS as sym
from ...models.boss import Boss
import time


class BossView(BaseView):
    @staticmethod
    def show_boss_encounter(boss: Boss):
        """Display thematic boss encounter screen"""
        BaseView.clear_screen()

        # Initial corruption warning
        print("\n" * 2)
        print(
            f"{dec['BOSS_ALERT']['START']} A Powerful Curse Approaches {dec['BOSS_ALERT']['END']}"
        )
        time.sleep(1.5)

        # Corruption visual effect
        for _ in range(3):
            print(
                f"\n{sym['CORRUPTION']} {sym['HOPE']} {sym['TAINT']} {sym['VOID']}",
                end="",
            )
            time.sleep(0.3)
            BaseView.clear_screen()
            print(
                f"\n{sym['VOID']} {sym['TAINT']} {sym['HOPE']} {sym['CORRUPTION']}",
                end="",
            )
            time.sleep(0.3)
            BaseView.clear_screen()

        # Boss name and title with thematic formatting
        print(f"\n{dec['CORRUPTION']['START']} {boss.name} {dec['CORRUPTION']['END']}")
        print(f"{sym['TITLE']} {boss.title} {sym['TITLE']}")

        # Show boss art with corruption effect
        art_lines = boss.art.split("\n")
        for line in art_lines:
            print(f"{sym['VOID']}{line}{sym['VOID']}")
            time.sleep(0.15)

        # Warning message matching the lore
        print(
            f"\n{dec['WARNING']['START']} Beware the touch of false hope! {dec['WARNING']['END']}"
        )

        input(
            f"\n{sym['VOID']} Steel your resolve and press Enter to face this corruption..."
        )
