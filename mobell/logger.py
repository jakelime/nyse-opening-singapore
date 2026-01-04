import logging
import os
from logging.handlers import RotatingFileHandler
from .config import get_path, settings


def setup_logging():
    """
    Configures the root logger to write to a rotating file and stdout.
    """
    log_dir = get_path("log_dirpath")

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "mobell.log")
    log_level_str = settings["config"].get("log_level", "INFO")
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    # 1. File Handler (Rotating: 1MB size, keep 5 backups)
    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    # 2. Console Handler (so you see output when running manually)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(
            "%(message)s"  # Simpler format for console
        )
    )

    # Setup Root Logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Avoid adding handlers multiple times if setup is called repeatedly
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
