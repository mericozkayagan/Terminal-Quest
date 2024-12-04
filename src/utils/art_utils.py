from ..utils.pixel_art import PixelArt
from typing import Tuple
import os
import logging


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


def load_ascii_art(filename: str) -> str:
    """Load ASCII art from file.

    Args:
        filename (str): Name of the art file (e.g., 'character_name.txt')

    Returns:
        str: ASCII art content or error message if file not found
    """
    # Clean up the filename
    clean_filename = os.path.basename(filename)

    # Ensure .txt extension
    if not clean_filename.endswith(".txt"):
        clean_filename += ".txt"

    # Construct the full path
    full_path = os.path.join("data/art", clean_filename)

    try:
        with open(full_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Could not find art file: {full_path}")
        return "ASCII art not found"


def draw_circle(
    art: "PixelArt", center_x: int, center_y: int, radius: int, color: tuple
) -> None:
    """Draw a circle on the pixel art.

    Args:
        art: PixelArt object to draw on
        center_x: X coordinate of circle center
        center_y: Y coordinate of circle center
        radius: Radius of the circle
        color: RGB color tuple (r, g, b)
    """
    for y in range(max(0, center_y - radius), min(art.height, center_y + radius + 1)):
        for x in range(
            max(0, center_x - radius), min(art.width, center_x + radius + 1)
        ):
            if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius**2:
                art.set_pixel(x, y, color)


def draw_rectangle(
    art: "PixelArt", x: int, y: int, width: int, height: int, color: tuple
) -> None:
    """Draw a filled rectangle on the pixel art.

    Args:
        art: PixelArt object to draw on
        x: Left coordinate
        y: Top coordinate
        width: Width of rectangle
        height: Height of rectangle
        color: RGB color tuple (r, g, b)
    """
    for cy in range(max(0, y), min(art.height, y + height)):
        for cx in range(max(0, x), min(art.width, x + width)):
            art.set_pixel(cx, cy, color)


def add_highlights(art: "PixelArt", color: tuple) -> None:
    """Add highlight effects to the pixel art.

    Args:
        art: PixelArt object to add highlights to
        color: RGB color tuple (r, g, b) for highlights
    """
    # Add highlights around the edges of existing pixels
    for y in range(art.height):
        for x in range(art.width):
            if art.pixels[y][x][3] > 0:  # If pixel is not empty
                # Add highlights to adjacent pixels
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < art.width
                        and 0 <= ny < art.height
                        and art.pixels[ny][nx][3] == 0
                    ):  # If adjacent pixel is empty
                        art.set_pixel(
                            nx, ny, color, alpha=0.5
                        )  # Semi-transparent highlight


def add_shadows(art: "PixelArt", color: tuple) -> None:
    """Add shadow effects to the pixel art.

    Args:
        art: PixelArt object to add shadows to
        color: RGB color tuple (r, g, b) for shadows
    """
    # Add shadows below and to the right of existing pixels
    for y in range(art.height - 1, -1, -1):  # Start from bottom
        for x in range(art.width):
            if art.pixels[y][x][3] > 0:  # If pixel is not empty
                # Add shadow to bottom-right pixels
                for dx, dy in [(1, 1), (0, 1), (1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < art.width
                        and 0 <= ny < art.height
                        and art.pixels[ny][nx][3] == 0
                    ):  # If adjacent pixel is empty
                        art.set_pixel(
                            nx, ny, color, alpha=0.3
                        )  # Semi-transparent shadow
