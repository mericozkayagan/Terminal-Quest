import logging
from typing import List, Optional

from src.models.skills import Skill

from .ai_generator import generate_character_class
from .art_generator import generate_class_art
from src.display.base.base_view import BaseView
from src.config.settings import ENABLE_AI_CLASS_GENERATION
from src.models.character import Player
from src.models.character_classes import get_default_classes, CharacterClass
from src.display.ai.ai_view import AIView
from src.display.character.character_view import CharacterView
from src.display.themes.dark_theme import DECORATIONS as dec
from src.utils.ascii_art import ensure_entity_art, load_ascii_art
import random

logger = logging.getLogger(__name__)


class CharacterCreationService:
    """Handles character creation logic"""

    @staticmethod
    def create_character(name: str) -> Optional[Player]:
        """Create a new player character"""
        if not name or len(name.strip()) == 0:
            return None

        try:
            # Get available classes
            classes = CharacterCreationService._get_character_classes()

            # Clear screen and show class selection
            BaseView.clear_screen()

            CharacterView.show_class_selection(classes)

            # Handle class selection
            chosen_class = CharacterCreationService._handle_class_selection(classes)
            if not chosen_class:
                return None

            # Create and return player
            return Player(name=name, char_class=chosen_class)

        except Exception as e:
            import traceback

            logger.error(f"Character creation error: {str(e)}")
            logger.error(traceback.format_exc())
            return None

    @staticmethod
    def _get_character_classes() -> List[CharacterClass]:
        """Get character classes based on configuration"""
        classes = []

        try:
            if ENABLE_AI_CLASS_GENERATION:
                AIView.show_generation_start("character classes")
                logger.info("Starting AI character class generation")

                for i in range(3):
                    try:
                        logger.info(f"Generating class {i+1}/3")
                        char_class = generate_character_class()
                        if char_class:
                            classes.append(char_class)
                            logger.info(
                                f"Successfully generated class: {char_class.name}"
                            )
                    except Exception as e:
                        logger.error(f"Failed to generate class {i+1}: {str(e)}")
                        continue

            # If AI generation is disabled or failed to generate enough classes,
            # use default classes
            if not ENABLE_AI_CLASS_GENERATION or len(classes) < 3:
                logger.info("Using default classes")
                default_classes = get_default_classes()
                # Only add enough default classes to reach 3 total
                needed = 3 - len(classes)
                classes.extend(default_classes[:needed])

            return classes

        except Exception as e:
            logger.error(f"Error in class generation: {str(e)}")
            logger.info("Falling back to default classes")
            return get_default_classes()[:3]

    @staticmethod
    def _validate_character_class(char_class: CharacterClass) -> bool:
        """Validate a character class has all required attributes"""
        required_attrs = [
            "name",
            "description",
            "base_health",
            "base_mana",
            "base_attack",
            "base_defense",
            "skills",
        ]

        try:
            for attr in required_attrs:
                if not hasattr(char_class, attr):
                    logger.error(f"Missing required attribute: {attr}")
                    return False

            if not isinstance(char_class.skills, list):
                logger.error("Skills must be a list")
                return False

            if not all(isinstance(skill, Skill) for skill in char_class.skills):
                logger.error("All skills must be Skill objects")
                return False

            return True
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False

    @staticmethod
    def _handle_class_selection(
        classes: List[CharacterClass],
    ) -> Optional[CharacterClass]:
        """Handle class selection input"""
        while True:
            try:
                choice = int(input("\nChoose your path (1-3): ")) - 1
                if 0 <= choice < len(classes):
                    return classes[choice]
                print("  Invalid choice. Choose between 1-3.")
            except ValueError:
                print("  Invalid input. Enter a number between 1-3.")
            except KeyboardInterrupt:
                return None

    @staticmethod
    def _ensure_class_art(char_class: CharacterClass) -> None:
        """Ensure character class has associated art"""
        if not hasattr(char_class, "art") or not char_class.art:
            art_file = ensure_entity_art(char_class.name, "class")
            if art_file:
                art_content = load_ascii_art(art_file)
                setattr(char_class, "art", art_content)
