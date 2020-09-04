import typing as t

import schema as sc

from .models import MindMap, Node


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self):
        self._call_stack = []

    @staticmethod
    def find_root_id(map_raw: t.List[t.Dict[str, t.Any]]) -> str:
        for record in map_raw:
            if "root" in record:
                return record["root"]

        raise ParsingError("Map root is not specified")

    def prepare_call_stack(self, map_raw: t.List[t.Dict[str, t.Any]]):
        root_id = self.find_root_id(map_raw)
        root_record = None

        for record in (r for r in map_raw if "root" not in r):
            if root_id in record:
                root_record = record
            else:
                self._call_stack.append((record, None))
        self._call_stack.append((root_record, None))

    def parse_map(self, map_raw: t.List[t.Dict[str, t.Any]]) -> MindMap:
        self.prepare_call_stack(map_raw)
        mind_map = MindMap(nodes={}, edges=[], root=None)

        while len(self._call_stack) > 0:
            record, parent_node = self._call_stack.pop()
            record = make_dict(record)

            validate_record(record, parent_node, mind_map)

            node_attrs = record.pop("attrs", {})
            node_name = list(record.keys())[0]
            node = mind_map.nodes.get(node_name)
            if node is not None:
                for attr_name, attr_val in node_attrs.items():
                    node.set(attr_name, attr_val)
            else:
                node = Node(node_name, parent_node, **node_attrs)

            node_children = list(record.values())[0] or []
            for child_record in node_children:
                self._call_stack.append((child_record, node))

            mind_map.nodes[node_name] = node
            if parent_node:
                mind_map.edges.append((parent_node, node))

        return mind_map


def make_dict(record: t.Union[str, t.Dict]) -> t.Dict[str, t.Any]:
    if not isinstance(record, dict):
        return {str(record): None}

    return record


def validate_record(record: t.Dict[str, t.Any], parent_node: t.Optional[Node], mind_map: MindMap):
    RecordSchema = sc.Schema({
        str: sc.Or(None, list),
        sc.Optional("attrs", default={}): sc.Schema({str: sc.Or(str, int, float, bool)})
    })
    meta_keys = {"attrs"}

    try:
        record = RecordSchema.validate(record)
    except sc.SchemaError as e:
        raise ParsingError(e)

    if len([k for k in record.keys() if k not in meta_keys]) > 1:
        raise ParsingError(f"Too much fields for node: {tuple(record.keys())}")

    node_name = list(record.keys())[0]
    if parent_node is None and node_name not in mind_map.nodes and len(mind_map.nodes) > 0:
        raise ParsingError(f"Node `{node_name}` is not connected to root")
