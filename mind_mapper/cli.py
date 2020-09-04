import click

from . import utils
from .renderer import render_map


@click.command()
@click.argument("map_path", type=click.Path(exists=True, readable=True))
@click.argument("output_path", type=click.Path(writable=True))
@click.option("-t", "--theme", "theme", type=str, default="mind_mapper.themes.default")
@click.option("-p", "--program", "program", type=str, default="dot")
@click.option("-f", "--format", "output_format", type=str, default="png")
def render(map_path, output_path, theme, program, output_format):
    map_raw = utils.load(map_path)
    styles_raw = utils.load(theme)

    status = render_map(map_raw, styles_raw, output_path, program, output_format)
    print("written:", status)
