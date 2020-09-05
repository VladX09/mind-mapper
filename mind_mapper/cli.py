import click
from loguru import logger

from . import utils
from .use_cases import render_map


@click.command()
@click.argument("map_path", type=click.Path(exists=True, readable=True, resolve_path=True))
@click.argument("output_path", type=click.Path(writable=True, resolve_path=True))
@click.option("-t", "--theme", "theme", type=str, default="mind_mapper.themes.default")
@click.option("-p", "--program", "program", type=str, default="dot")
@click.option("-f", "--format", "output_format", type=str, default="png")
@click.option("--logs", "enable_logs", is_flag=True)
def render(map_path, output_path, theme, program, output_format, enable_logs):
    if enable_logs:
        logger.enable("mind_mapper")

    map_raw = utils.load(map_path)
    styles_raw = utils.load(theme)

    write_success = render_map(map_raw, styles_raw, output_path, program, output_format)

    if write_success:
        click.echo(f"'{output_path}': written")
    else:
        click.echo(f"'{output_path}': error")
        exit(1)
