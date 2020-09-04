import click

from . import utils
from .renderer import render_map


@click.command()
@click.argument("map_path", type=click.Path(exists=True, readable=True))
@click.argument("output_path", type=click.Path(exists=True, readable=True, writable=True))
@click.option("--theme", "theme", type=str, default="themes.default")
def render(map_path, output_path, theme):
    map_raw = utils.load(map_path)
    styles_raw = utils.load(theme)

    status = render_map(map_raw, styles_raw, output_path)
    print("written:", status)
