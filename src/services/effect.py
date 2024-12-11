from typing import Dict, List, Optional, Type
from ..models.effects.base import BaseEffect
from ..models.character import Character
from ..config.settings import GAME_BALANCE
from ..display.effect.effect_view import EffectView
from ..models.base_types import EffectTrigger
import random
import logging

logger = logging.getLogger(__name__)


class EffectService:
    """Centralized service for managing game effects"""

    def __init__(self):
        self.effect_view = EffectView()

    def create_effect(self, effect_type: Type[BaseEffect], **kwargs) -> BaseEffect:
        """Factory method for creating effects with proper scaling"""
        try:
            if "potency" in kwargs:
                kwargs["potency"] *= GAME_BALANCE["EFFECT_SCALING"][
                    effect_type.__name__
                ]
            return effect_type(**kwargs)
        except Exception as e:
            logger.error(f"Failed to create effect {effect_type}: {e}")
            raise

    def apply_effect(
        self, effect: BaseEffect, target: Character, source: Optional[Character] = None
    ) -> Dict:
        """Apply effect with resistance checks and visualization"""
        if self._check_resistance(target, effect):
            self.effect_view.show_resist(target, effect)
            return {"success": False, "resisted": True}

        result = target.add_effect(effect, source)
        if result["success"]:
            self.effect_view.show_effect_applied(target, effect)

        return result

    def process_combat_effects(
        self, attacker: Character, defender: Character, damage: int
    ) -> List[Dict]:
        """Process all combat-related effects"""
        results = []

        # Process ON_HIT effects
        results.extend(
            self._process_trigger(
                attacker, EffectTrigger.ON_HIT, target=defender, damage=damage
            )
        )

        # Process ON_HIT_TAKEN effects
        results.extend(
            self._process_trigger(
                defender, EffectTrigger.ON_HIT_TAKEN, source=attacker, damage=damage
            )
        )

        return results

    def update_effect_durations(self, character: Character) -> List[Dict]:
        """Update effect durations and remove expired effects"""
        expired = []
        messages = []

        for effect in character.get_all_effects():
            if effect.duration > 0:
                effect.duration -= 1
                if effect.duration <= 0:
                    expired.append(effect)

        for effect in expired:
            result = character.remove_effect(effect)
            messages.append(result)
            self.effect_view.show_effect_expired(character, effect)

        return messages

    def _check_resistance(self, target: Character, effect: BaseEffect) -> bool:
        """Check if effect is resisted"""
        resistance = target.get_resistance(effect.effect_type)
        return random.random() < resistance

    def _process_trigger(
        self, character: Character, trigger: EffectTrigger, **kwargs
    ) -> List[Dict]:
        """Process all effects for a given trigger"""
        results = []
        for effect in character.get_effects_by_trigger(trigger):
            try:
                result = effect.apply(character, **kwargs)
                if result.get("success", False):
                    self.effect_view.show_effect_trigger(character, effect, result)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing effect {effect.name}: {e}")
        return results
