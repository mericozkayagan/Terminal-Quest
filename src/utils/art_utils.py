from ..utils.pixel_art import PixelArt
from typing import Tuple


def draw_circular_shape(
    art: PixelArt, cx: int, cy: int, color: Tuple[int, int, int], char: str
):
    radius = min(art.width, art.height) // 4
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= radius**2:
                art.set_pixel(x, y, color, char=char)


def draw_tall_shape(
    art: PixelArt, cx: int, cy: int, color: Tuple[int, int, int], char: str
):
    width = art.width // 3
    height = art.height // 2
    for y in range(cy - height, cy + height):
        for x in range(cx - width, cx + width):
            art.set_pixel(x, y, color, char=char)


def add_feature(art: PixelArt, feature: str, color: Tuple[int, int, int], char: str):
    if "glowing" in feature.lower():
        add_glow_effect(art, color, char)
    elif "spiky" in feature.lower():
        add_spikes(art, color, char)


def add_detail(art: PixelArt, detail: str, color: Tuple[int, int, int], char: str):
    # Add basic detail implementation
    center_x, center_y = art.width // 2, art.height // 2
    art.set_pixel(center_x, center_y, color, char=char)


def draw_default_shape(
    art: PixelArt, cx: int, cy: int, color: Tuple[int, int, int], char: str
):
    """Draw default rectangular shape"""
    width = art.width // 3
    height = art.height // 2
    for y in range(cy - height // 2, cy + height // 2):
        for x in range(cx - width // 2, cx + width // 2):
            if 0 <= x < art.width and 0 <= y < art.height:
                art.set_pixel(x, y, color, char=char)


def add_glow_effect(art, x, y, color):
    """Add a glowing effect to the pixel art."""
    # Implementation here
    pass


def add_spikes(art, x, y, color):
    """Add spikes to the pixel art."""
    # Implementation here
    pass
