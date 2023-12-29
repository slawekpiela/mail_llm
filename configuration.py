from enum import Enum

import tomli


class Models(Enum):
    """
    Słownik modeli do wykorzystania
    dostęp w kodzie:
    Models.GPT_TURBO.value
    """
    GPT3 = "gpt-3.5-turbo-1106"
    GPT4 = "gpt-4-1106-preview"


def _get_config():
    """
    Module runs in context of the root folder with pyproject.toml file
    """
    with open("secrets.toml", "rb") as f:
        config = tomli.load(f)

    return config


_config = _get_config()
api_key = _config["API"]["key"]
assistant_id = _config["API"]["assistant_id"]
sender_passwords = _config["Mail"]["sender_passwords"]
user_mailin = _config["Mail"]["user_mailin"]
engine = _config["Engines"]["GPT4"]
