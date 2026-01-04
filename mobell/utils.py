import os
import subprocess
import requests
import logging
from .config import get_path

logger = logging.getLogger(__name__)


def play_bell():
    """
    Plays the bell sound defined in config.
    Downloads a default if the file is missing.
    """
    # Get path from config and expand ~
    sound_path = get_path("bell_filepath")

    # Ensure the directory for the sound file exists
    os.makedirs(os.path.dirname(sound_path), exist_ok=True)

    # Download if missing
    if not os.path.exists(sound_path):
        logger.info(f"Sound file not found at {sound_path}. Downloading default...")
        try:
            url = "https://actions.google.com/sounds/v1/alarms/mechanic_clock_ring.ogg"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(sound_path, "wb") as f:
                    f.write(response.content)
                logger.info("Default sound downloaded successfully.")
            else:
                logger.error(
                    f"Failed to download sound. Status: {response.status_code}"
                )
                return
        except Exception as e:
            logger.error(f"Error downloading sound: {e}")
            return

    # Play the sound
    logger.info(f"Playing sound: {sound_path}")
    try:
        subprocess.run(["afplay", sound_path], check=True)
    except FileNotFoundError:
        logger.error("Error: 'afplay' command not found. Are you on macOS?")
    except Exception as e:
        logger.error(f"Error playing sound: {e}")
