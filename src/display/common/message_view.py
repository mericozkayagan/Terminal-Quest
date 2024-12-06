from ..themes.dark_theme import DECORATIONS as dec


class MessageView:
    """Handles general message display logic"""

    @staticmethod
    def show_error(message: str):
        """Display error message"""
        print(f"\n{dec['SECTION']['START']}Error{dec['SECTION']['END']}")
        print(f"  {message}")

    @staticmethod
    def show_success(message: str):
        """Display success message"""
        print(f"\n{dec['SECTION']['START']}Success{dec['SECTION']['END']}")
        print(f"  {message}")

    @staticmethod
    def show_info(message: str):
        """Display information message"""
        print(f"\n{dec['SECTION']['START']}Notice{dec['SECTION']['END']}")
        print(f"  {message}")
