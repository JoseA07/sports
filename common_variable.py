import os
import json
from dotenv import load_dotenv


def get_env_variable(key):
    """Load the .env file and return the value of the given key."""
    load_dotenv()
    return os.getenv(key)


def load_config(filename):
    """Load configuration from a JSON file."""
    with open(filename, "r") as file:
        config = json.load(file)
    return config
