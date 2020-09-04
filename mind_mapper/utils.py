import os
import sys
from importlib import resources as importlib_resources

import yaml
from loguru import logger


def load(path):
    if os.path.exists(path):
        with open(path) as fp:
            return yaml.full_load(fp)

    package, name = path.rsplit(".", 1)
    name = f"{name}.yml"

    try:
        with importlib_resources.open_text(package, name) as fp:
            return yaml.full_load(fp)

    except FileNotFoundError:
        raise ValueError(f"Unknown or non-existing path: '{path}'.")


config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": (
                "{time:YYYY-MM-DD HH:mm:ss}"
                " | <level>{level: <4}</level>"
                " | <c>{name}</c>:<c>{function}</c>:<c>{line}</c> - <level>{message}</level>"
            ),
        }
    ]
}

logger.configure(**config)  # type: ignore
