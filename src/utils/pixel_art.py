from dataclasses import dataclass
from typing import List, Tuple
import random


@dataclass
class Pixel:
    char: str
    fg_color: Tuple[int, int, int]
    bg_color: Tuple[int, int, int] = (0, 0, 0)


class PixelArt:
    def __init__(self, width: int, height: int):
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Width and height must be integers")
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
        self.width = width
        self.height = height
        self.pixels: List[List[Pixel]] = [
            [Pixel("▀", (0, 0, 0)) for _ in range(width)] for _ in range(height)
        ]

    def set_pixel(
        self,
        x: int,
        y: int,
        fg_color: Tuple[int, int, int],
        bg_color: Tuple[int, int, int] = (0, 0, 0),
        char: str = "▀",
    ):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = Pixel(char, fg_color, bg_color)

    def render(self) -> str:
        output = []
        for row in self.pixels:
            line = []
            for pixel in row:
                fg_r, fg_g, fg_b = pixel.fg_color
                bg_r, bg_g, bg_b = pixel.bg_color
                line.append(
                    f"\x1b[38;2;{fg_r};{fg_g};{fg_b}m"
                    f"\x1b[48;2;{bg_r};{bg_g};{bg_b}m{pixel.char}"
                )
            output.append("".join(line) + "\x1b[0m")
        return "\n".join(output)
