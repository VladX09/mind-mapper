import abc
import re
import typing as t

from models import Node
NODE_PLACEHOLDER = "NODE"


class Predicate(abc.ABC):
    @abc.abstractmethod
    def __call__(self, node: Node) -> bool:
        ...


class EvalPredicate(Predicate):
    def __init__(self, target: str) -> None:
        self._target = target

    def __call__(self, node: Node) -> bool:
        return bool(eval(self._target, {NODE_PLACEHOLDER: node}))


class RegexPredicate(Predicate):
    def __init__(self, target: str, pattern: str) -> None:
        self._target = target
        self._pattern = pattern

    def __call__(self, node: Node) -> bool:
        target_val = str(eval(self._target, {NODE_PLACEHOLDER: node}))
        return re.match(self._pattern, target_val) is not None


class NamePredicate(RegexPredicate):
    def __init__(self, pattern: str) -> None:
        target = f"{NODE_PLACEHOLDER}.get_name()"
        super().__init__(target, pattern)


class Style:
    def __init__(self, name: str, predicate: Predicate, attrs: t.Dict[str, t.Any], priority: int = 0) -> None:
        self.name = name
        self.predicate = predicate
        self.attrs = attrs
        self.priority = priority

    def apply(self, node: Node) -> None:
        if self.predicate(node):
            node.attrs.update(self.attrs)
