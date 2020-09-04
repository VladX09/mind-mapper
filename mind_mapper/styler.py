import abc
import re
import typing as t

from models import Node
NODE_PLACEHOLDER = "NODE"


class Predicate(abc.ABC):
    def __init__(self, priority: int = 0) -> None:
        self._priority = priority

    @abc.abstractmethod
    def __call__(self, node: Node) -> bool:
        ...


class EvalPredicate(Predicate):
    def __init__(self, target: str, priority: int = 0) -> None:
        super().__init__(priority=priority)
        self._target = target

    def __call__(self, node: Node) -> bool:
        return bool(eval(self._target, {NODE_PLACEHOLDER: node}))


class RegexPredicate(Predicate):
    def __init__(self, target: str, pattern: str, priority: int = 0) -> None:
        super().__init__(priority=priority)
        self._target = target
        self._pattern = pattern

    def __call__(self, node: Node) -> bool:
        target_val = str(eval(self._target, {NODE_PLACEHOLDER: node}))
        return re.match(self._pattern, target_val) is not None


class NamePredicate(RegexPredicate):
    def __init__(self, pattern: str, priority: int = 0) -> None:
        target = f"{NODE_PLACEHOLDER}.get_name()"
        super().__init__(target, pattern, priority)
