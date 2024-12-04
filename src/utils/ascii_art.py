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

def load_ascii_art(filename: str) -> str:
    """Load ASCII art from a file.
    
    Args:
        filename: Source filename
    
    Returns:
        ASCII art string
    
    Raises:
        ValueError: If filename is invalid
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    if not filename or not filename.strip():
        raise ValueError("Invalid filename")
    
    safe_path = os.path.abspath(os.path.join(os.getcwd(), filename))
    if not safe_path.startswith(os.getcwd()):
        raise ValueError("Invalid file path")
    
    if not os.path.exists(safe_path):
        raise FileNotFoundError(f"File not found: {filename}")
    
    try:
        with open(safe_path, "r") as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Failed to load ASCII art: {e}")

def display_ascii_art(ascii_art):
    """Display ASCII art in the terminal."""
    print(ascii_art)
