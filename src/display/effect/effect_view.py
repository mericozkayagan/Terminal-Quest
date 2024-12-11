from typing import Dict
from ..base.base_view import BaseView
from ...models.effects.base import BaseEffect
from ...models.character import Character
from ...display.themes.dark_theme import SYMBOLS as sym


class EffectView(BaseView):
    """Handles visualization of effects"""

    def show_effect_applied(self, target: Character, effect: BaseEffect):
        """Display effect application"""
        symbol = self._get_effect_symbol(effect)
        self.print_colored(
            f"{symbol} {target.name} gains {effect.name}",
            self._get_effect_color(effect),
        )

    def show_effect_trigger(
        self, character: Character, effect: BaseEffect, result: Dict
    ):
        """Display effect trigger"""
        if "damage" in result:
            self._show_damage_effect(character, effect, result["damage"])
        elif "healing" in result:
            self._show_healing_effect(character, effect, result["healing"])
        else:
            self.print_colored(
                f"{self._get_effect_symbol(effect)} {result['message']}",
                self._get_effect_color(effect),
            )

    def show_effect_expired(self, target: Character, effect: BaseEffect):
        """Display effect expiration"""
        self.print_colored(
            f"{sym['effect_expire']} {effect.name} fades from {target.name}",
            "dark_gray",
        )

    def show_resist(self, target: Character, effect: BaseEffect):
        """Display effect resistance"""
        self.print_colored(
            f"{sym['resist']} {target.name} resists {effect.name}!", "yellow"
        )

    def _get_effect_symbol(self, effect: BaseEffect) -> str:
        """Get appropriate symbol for effect type"""
        return {
            "STATUS": sym["status"],
            "SET_BONUS": sym["set_bonus"],
            "ITEM_TRIGGER": sym["trigger"],
            "STAT_MODIFIER": sym["stat"],
        }.get(effect.effect_type.value, sym["effect"])

    def _get_effect_color(self, effect: BaseEffect) -> str:
        """Get appropriate color for effect type"""
        return {
            "STATUS": "red",
            "SET_BONUS": "blue",
            "ITEM_TRIGGER": "green",
            "STAT_MODIFIER": "cyan",
        }.get(effect.effect_type.value, "white")
