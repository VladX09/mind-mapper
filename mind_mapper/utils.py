import os
from importlib import resources as importlib_resources

import yaml
from loguru import logger


def load(path):
    if os.path.exists(path):
        path = os.path.abspath(path)

        logger.debug("Loading from '{}'", path)
        with open(path) as fp:
            return yaml.full_load(fp)

    package, name = path.rsplit(".", 1)
    name = f"{name}.yml"

    try:
        with importlib_resources.open_text(package, name) as fp:
            logger.debug("Loading from '{}' in package '{}'", name, package)
            return yaml.full_load(fp)

    except FileNotFoundError:
        raise ValueError(f"Unknown or non-existing path: '{path}'.")
