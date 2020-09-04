import yaml


def load(path):
    with open(path) as fp:
        return yaml.full_load(fp)
