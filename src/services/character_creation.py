from typing import List, Optional
from src.config.settings import ENABLE_AI_CLASS_GENERATION
from src.models.character import Player
from src.models.character_classes import get_default_classes, CharacterClass
from src.display.ai.ai_view import AIView
from src.display.character.character_view import CharacterView
from src.display.themes.dark_theme import DECORATIONS as dec
from src.utils.ascii_art import ensure_character_art, load_ascii_art


class CharacterCreationService:
    """Handles character creation logic"""

    @staticmethod
    def create_character(name: str) -> Optional[Player]:
        """Create a new player character"""
        if not name or len(name.strip()) == 0:
            return None

        # Get and display available classes
        classes = CharacterCreationService._get_character_classes()
        CharacterView.show_class_selection(classes)

        # Handle class selection
        chosen_class = CharacterCreationService._handle_class_selection(classes)
        if not chosen_class:
            return None

        # Load or generate character art
        CharacterCreationService._ensure_class_art(chosen_class)

        # Show final character details
        CharacterView.show_character_class(chosen_class)

        return Player(name=name, char_class=chosen_class)

    @staticmethod
    def _get_character_classes() -> List[CharacterClass]:
        """Get character classes based on configuration"""
        classes = get_default_classes()

        if ENABLE_AI_CLASS_GENERATION:
            AIView.show_generation_start("character class")
            # AI generation would go here
            AIView.show_generation_result("Generated custom classes")
        else:
            print(f"\n{dec['SECTION']['START']}Notice{dec['SECTION']['END']}")
            print("  Using default character classes...")

        return classes

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
            art_file = ensure_character_art(char_class.name)
            if art_file:
                art_content = load_ascii_art(art_file)
                setattr(char_class, "art", art_content)
