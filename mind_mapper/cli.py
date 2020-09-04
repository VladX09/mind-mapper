import click

from . import utils
from .renderer import render_map


@click.command()
@click.argument("map_path", type=click.Path(exists=True, readable=True))
@click.argument("output_path", type=click.Path(exists=True, readable=True, writable=True))
@click.option("--styles", "styles_path", type=click.Path(exists=True, readable=True), default=None)
def render(map_path, output_path, styles_path):
    map_raw = utils.load(map_path)
    styles_raw = utils.load(styles_path)

    status = render_map(map_raw, styles_raw, output_path)
    print("written:", status)
