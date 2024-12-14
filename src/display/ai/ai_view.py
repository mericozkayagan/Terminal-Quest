from src.display.themes.dark_theme import SYMBOLS as sym
from src.display.themes.dark_theme import DECORATIONS as dec


class AIView:
    """Handles AI-related display logic"""

    @staticmethod
    def show_generation_start(entity_type: str):
        """Display generation start message"""
        print(
            f"\n{dec['TITLE']['PREFIX']}Generating {entity_type}{dec['TITLE']['SUFFIX']}"
        )
        print(f"{dec['SEPARATOR']}")
        print("\nGenerating content...")

    @staticmethod
    def show_generation_result(content: str):
        """Display generated content"""
        print(f"\n{dec['SECTION']['START']}Generation Complete{dec['SECTION']['END']}")
        print(f"\n{content}")

    @staticmethod
    def show_error(error_msg: str):
        """Display AI generation error"""
        print(f"\n{dec['SECTION']['START']}Generation Failed{dec['SECTION']['END']}")
        print(f"  {error_msg}")
