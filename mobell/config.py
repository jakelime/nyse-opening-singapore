import os
import tomlkit
from pathlib import Path

# Define the base directory (root of the app)
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.toml"

# Default configuration structure
DEFAULT_CONFIG = {
    "config": {
        # Using expandable user paths for flexibility
        "bell_filepath": "~/apps/nyse-opening-singapore/resources/bell.wav",
        "log_dirpath": "~/apps/nyse-opening-singapore/logs/",
        "log_level": "INFO",
    }
}


def load_config():
    """
    Loads config from config.toml.
    If it doesn't exist, creates it with defaults.
    """
    if not CONFIG_PATH.exists():
        return create_default_config()

    try:
        with open(CONFIG_PATH, "r") as f:
            return tomlkit.load(f)
    except Exception as e:
        print(f"Error loading config.toml: {e}. Using defaults.")
        return DEFAULT_CONFIG


def create_default_config():
    """
    Creates the config.toml file with documented defaults.
    """
    doc = tomlkit.document()
    doc.add(tomlkit.comment("Configuration for NYSE Opening Bell"))

    config_section = tomlkit.table()
    config_section.add(tomlkit.comment("Path to the sound file to play"))
    config_section["bell_filepath"] = DEFAULT_CONFIG["config"]["bell_filepath"]

    config_section.add(tomlkit.comment("Directory where logs will be stored"))
    config_section["log_dirpath"] = DEFAULT_CONFIG["config"]["log_dirpath"]

    config_section["log_level"] = DEFAULT_CONFIG["config"]["log_level"]

    doc["config"] = config_section

    with open(CONFIG_PATH, "w") as f:
        f.write(doc.as_string())

    return doc


# Singleton-like access to config
settings = load_config()


def get_path(key):
    """
    Helper to get a path from config and expand the user (~).
    """
    raw_path = settings["config"].get(key)
    return os.path.expanduser(raw_path)
