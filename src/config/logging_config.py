"""Logging configuration for the game."""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging(debug_mode: bool = False) -> None:
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"debug_{timestamp}.log"

    # Set up basic configuration
    level = logging.DEBUG if debug_mode else logging.INFO

    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),  # Also output to console
        ],
    )

    # Create loggers for different components
    loggers = {
        "ai": logging.getLogger("ai"),
        "game": logging.getLogger("game"),
        "combat": logging.getLogger("combat"),
        "character": logging.getLogger("character"),
    }

    # Configure all loggers
    for logger in loggers.values():
        logger.setLevel(level)
