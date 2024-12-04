import os
import sys
import time
from ..config.settings import DISPLAY_SETTINGS


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def type_text(text: str, delay: float = None):
    """Print text with a typewriter effect."""
    if delay is None:
        delay = DISPLAY_SETTINGS["TYPE_SPEED"]

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
