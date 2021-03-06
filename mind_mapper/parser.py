import typing as t

import schema as sc
from loguru import logger

from . import schemas
from .models import MindMap, Node


class ParsingError(Exception):
    pass


class Parser:
    """Parses YAML map description to lists of nodes and edges.

    Tracks node parent, children, depth and initial styles.
    """
    def __init__(self):
        self._call_stack = []

    @staticmethod
    def find_root_id(map_raw: t.List[t.Dict[str, t.Any]]):
        for record in map_raw:
            if "root" in record:
                return record["root"]

        raise ParsingError("Map root is not specified")

    def prepare_call_stack(self, map_raw: t.List[t.Dict[str, t.Any]]):
        """Initializes call stack with first level YAML entities and root on the top."""
        root_id = self.find_root_id(map_raw)
        root_record = None

        for record in (r for r in map_raw if "root" not in r):
            if root_id in record:
                root_record = record
            else:
                self._call_stack.append((record, None))

        # We sholud start iteration from the root
        self._call_stack.append((root_record, None))

    def parse_map(self, map_raw: t.List[t.Dict[str, t.Any]]) -> MindMap:
        try:
            map_raw = schemas.MapSchema.validate(map_raw)
            self.prepare_call_stack(map_raw)
            mind_map = MindMap(nodes={}, edges=[], root=None)

            while len(self._call_stack) > 0:
                record, parent_node = self._call_stack.pop()
                record = make_dict(record)

                validate_record(record, parent_node, mind_map)

                node_attrs = record.pop("attrs", {})
                node_name = list(record.keys())[0]

                # Checking if we saw this node previously in the file
                node = mind_map.nodes.get(node_name)
                if node is not None:
                    node.init_attrs.update(node_attrs)
                else:
                    node = Node(node_name, parent_node, **node_attrs)

                node_children = list(record.values())[0] or []
                for child_record in node_children:
                    self._call_stack.append((child_record, node))

                mind_map.nodes[node_name] = node
                if parent_node:
                    mind_map.edges.append((parent_node, node))
                    parent_node.children.append(node)

        except sc.SchemaError as e:
            raise ParsingError(e)

        return mind_map


def make_dict(record: t.Union[str, t.Dict]) -> t.Dict[str, t.Any]:
    """Parse nodes without children and attributes."""
    if not isinstance(record, dict):
        return {str(record): None}

    return record


def validate_record(record: t.Dict[str, t.Any], parent_node: t.Optional[Node], mind_map: MindMap):
    logger.debug("Validation: {}", record)
    meta_keys = {"attrs"}
    record = schemas.RecordSchema.validate(record)

    if len([k for k in record.keys() if k not in meta_keys]) > 1:
        raise ParsingError(f"Too much fields for node: {tuple(record.keys())}")

    node_name = list(record.keys())[0]
    if parent_node is None and node_name not in mind_map.nodes and len(mind_map.nodes) > 0:
        raise ParsingError(f"Node `{node_name}` is not connected to root")
