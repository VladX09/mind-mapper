import typing as t

import pydot


class Node(pydot.Node):
    def __init__(self, name: str, parent: "Node", **attrs):
        super().__init__(name, **attrs)
        self.parent = parent
        self.depth: int = parent.depth + 1 if parent else 0

    def __str__(self):
        return f"Node({self.get_name()}, {self.depth})"


class MindMap:
    def __init__(self, nodes: t.Dict[str, Node], edges: t.List[t.Tuple[Node, Node]], root: t.Optional[Node]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.root = root
