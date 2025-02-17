from zql.grammar import Grammar
from zql.parser import AstNode
from zql.types import SqlQuery


RuleKey = tuple[str, list[str]]
Template = str
TemplateLookup = dict[RuleKey, Template]


SPACE = " "
SEQUENCE_RULE_TYPE = "sequence"
NON_CHILDREN_RULE_TYPES = {"literal", "regex"}


class QueryRenderError(Exception):
    pass


def render_query(grammar: Grammar, ast: AstNode) -> SqlQuery:
    template_lookup = get_template_lookup(grammar)
    return render_with_grammar(grammar, template_lookup, ast)


def render_with_grammar(
    grammar: Grammar,
    lookup: TemplateLookup,
    ast: AstNode
) -> SqlQuery:
    node_type = ast.get("type")
    children = ast.get("children", [])
    if not node_type:
        raise QueryRenderError(f"Node should have a `type`: {ast}")

    template = maybe_get_template(lookup, ast)
    if template:
        kwargs = {
            c.get("type"): render_with_grammar(grammar, lookup, c)
            for c in children
        }
        rendered = template.format(**kwargs)
        return rendered

    if children:
        args = [render_with_grammar(grammar, lookup, c) for c in children]
        rendered = SPACE.join(args)
        return rendered

    value = ast.get("value")
    if value is not None:
        return value

    raise QueryRenderError(f"Unable to render node: `{node_type}`.")


def get_template_lookup(grammar: Grammar) -> TemplateLookup:
    template_lookup: TemplateLookup = {}
    for node, rules in grammar.items():
        for rule in rules:
            template = rule.get("template")
            if template is None:
                continue

            key = get_rule_key(node, rule)
            template_lookup[key] = template

    return template_lookup


def get_rule_key(node: str, rule: dict) -> RuleKey:
    if SEQUENCE_RULE_TYPE in rule:
        sequence = rule.get(SEQUENCE_RULE_TYPE)
        key = SPACE.join([node, *sequence])
        return key

    for rule_type in NON_CHILDREN_RULE_TYPES:
        if rule_type in rule:
            key = SPACE.join([node, rule_type])
            return key

    raise QueryRenderError(f"Unable to determine pattern of node: `{node}`.")


def maybe_get_template(lookup: TemplateLookup, ast: AstNode) -> Template | None:
    node = ast.get("type")
    children = ast.get("children", [])

    if children:
        rule_pattern = [child.get("type") for child in children]
        key = SPACE.join([node, *rule_pattern])
        template = lookup.get(key)
        return template

    for rule_type in NON_CHILDREN_RULE_TYPES:
        key = SPACE.join([node, rule_type])
        template = lookup.get(key)
        if template is not None:
            return template

    return None
