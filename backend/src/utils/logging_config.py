import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logging(log_level: str = "INFO", log_file: str = None):
    """
    Set up logging configuration for the application.
    """
    # Create logger
    logger = logging.getLogger("todo_app")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if specified
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Create a global logger instance
logger = setup_logging(
    log_level="INFO",
    log_file="logs/app.log"
)