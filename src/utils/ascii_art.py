import os


def convert_pixel_art_to_ascii(pixel_art):
    """Convert pixel art to ASCII art."""
    ascii_art = ""
    for row in pixel_art:
        for pixel in row:
            if pixel == 0:
                ascii_art += " "
            else:
                ascii_art += "#"
        ascii_art += "\n"
    return ascii_art


def save_ascii_art(ascii_art, filename):
    """Save ASCII art to a file."""
    with open(filename, "w") as file:
        file.write(ascii_art)


def load_ascii_art(filename):
    """Load ASCII art from a file."""
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as file:
        return file.read()


def display_ascii_art(ascii_art):
    """Display ASCII art in the terminal."""
    print(ascii_art)
