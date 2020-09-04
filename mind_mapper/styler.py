import abc
import re
import typing as t

import schema as sc

from models import Node

from . import schemas

NODE_PLACEHOLDER = "NODE"


class StyleParsingError(Exception):
    pass


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


class PredicateFabric:
    constructors = {
        "eval": EvalPredicate,
        "regex": RegexPredicate,
        "name": NamePredicate,
    }

    def __call__(self, predicate_raw: t.Dict[str, t.Any]) -> Predicate:
        constructor = self.constructors[predicate_raw["type"]]
        params = {k: v for k, v in predicate_raw.items() if k != "type"}

        return constructor(**params)


class Style:
    def __init__(self, name: str, predicate: Predicate, attrs: t.Dict[str, t.Any], order: int = 0) -> None:
        self.name = name
        self.predicate = predicate
        self.attrs = attrs
        self.order = order

    def apply(self, node: Node) -> None:
        if self.predicate(node):
            node.attrs.update(self.attrs)


def parse_styles(styles: t.Dict[str, t.Dict]) -> t.List[Style]:
    styles_parsed: t.List[Style] = []
    predicate_fabric = PredicateFabric()

    try:
        for style_name, style in styles.items():
            style = schemas.StyleSchema.validate(style)
            style["predicate"] = predicate_fabric(style["predicate"])
            style_obj = Style(style_name, **style)

            styles_parsed.append(style_obj)

    except sc.SchemaError as e:
        raise StyleParsingError(e)

    return sorted(styles_parsed, key=lambda x: x.order)
