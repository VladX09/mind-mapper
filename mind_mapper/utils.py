import importlib
import os

import yaml


def load(path):
    if os.path.exists(path):
        with open(path) as fp:
            return yaml.full_load(fp)

    package, name = path.rsplit(".", 1)

    try:
        with importlib.resources.open_text(package, name) as fp:
            return yaml.full_load(fp)

    except FileNotFoundError:
        raise ValueError(f"Unknown or non-existing path: '{path}'.")
