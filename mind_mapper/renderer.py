import pydot
import typing as t

from . import parser, styler


def render_map(map_raw: t.List[t.Dict[str, t.Any]], styles_raw: t.Dict[str, t.Dict], output_path: str):
    map_parser = parser.Parser()
    mind_map = map_parser.parse_map(map_raw)

    styles = styler.parse_styles(styles_raw)
    styler.apply_styles(styles, mind_map)

    for node in mind_map.nodes.values():
        node.finalize_attrs()

    graph = pydot.Dot(overlap=False, sep="+20,40", graph_type="digraph", pad=0.5)

    for node in mind_map.nodes.values():
        graph.add_node(node)

    for edge in mind_map.edges:
        graph.add_edge(pydot.Edge(*edge))

    return graph.write(output_path, prog="circo", format="png")
