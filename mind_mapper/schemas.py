import schema as sc

AttrsSchema = sc.Schema({sc.Optional(str): sc.Or(str, int, float, bool)})
RecordSchema = sc.Schema({
    str: sc.Or(None, list),
    sc.Optional("attrs", default={}): AttrsSchema,
})
RootSchema = sc.Schema({"root": str, sc.Optional("attrs"): AttrsSchema})
MapSchema = sc.Schema([sc.Or(RecordSchema, RootSchema)])
EvalPredicateSchema = sc.Schema({
    "type": "eval",
    "target": str,
})
RegexPredicateSchema = sc.Schema({
    "type": "regex",
    "target": str,
    "pattern": str,
})
NamePredicateSchema = sc.Schema({
    "type": "name",
    "pattern": str,
})
PredicateSchema = sc.Or(EvalPredicateSchema, RegexPredicateSchema, NamePredicateSchema)
StyleSchema = sc.Schema({
    "predicate": PredicateSchema,
    "attrs": AttrsSchema,
    sc.Optional("order", default=0): int,
})
