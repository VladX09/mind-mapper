import typing as t

import pydot


class Node(pydot.Node):
    def __init__(self, name: str, parent: "Node", children: t.Optional[t.List["Node"]] = None, **init_attrs):
        super().__init__(name)
        self.parent = parent
        self.depth: int = parent.depth + 1 if parent else 0

        self.children = children or []
        self.init_attrs = init_attrs
        self.theme_attrs: t.Dict[str, t.Any] = {}

    @property
    def attrs(self) -> t.Dict[str, t.Any]:
        return {**self.theme_attrs, **self.init_attrs}

    def finalize_attrs(self):
        for name, val in self.attrs.items():
            self.set(name, val)


class MindMap:
    def __init__(self, nodes: t.Dict[str, Node], edges: t.List[t.Tuple[Node, Node]], root: t.Optional[Node]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.root = root
