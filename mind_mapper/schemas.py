import schema as sc

AttrsSchema = sc.Schema({str: sc.Or(str, int, float, bool)})
RecordSchema = sc.Schema({
    str: sc.Or(None, list),
    sc.Optional("attrs", default={}): AttrsSchema,
})
MapSchema = sc.Schema([sc.Or(RecordSchema, {"root": str})])
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