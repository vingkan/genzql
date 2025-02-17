import re
from zql.grammar import ROOT, Grammar
from zql.cleaner import get_tokens_string_safe


SPACE = " "


AstNode = dict


class AstParseError(Exception):
    pass


class TokensManager:

    def __init__(self, tokens: list[str]):
        self.tokens = tokens

    def set_tokens(self, tokens: list[str]):
        self.tokens = tokens

    def copy(self):
        return TokensManager(list(self.tokens))


def evaluate_literal(tokens: list[str], literal: str) -> AstNode:
    tokens_in_literal = len(literal.split(SPACE))
    peeked_tokens = SPACE.join(tokens[:tokens_in_literal]).casefold()
    if peeked_tokens != literal:
        raise AstParseError(f"Expected `{literal}`. Got `{peeked_tokens}`.")
    
    for _ in range(tokens_in_literal):
        tokens.pop(0)
    return {"value": literal}


def evaluate_regex(tokens: list[str], regex: str) -> AstNode:
    if not tokens:
        raise AstParseError(f"Expected match for `{regex}`, not end of input.")

    next_token = tokens[0]
    if not re.compile(regex).match(next_token):
        raise AstParseError(f"Expected `{next_token}` to match `{regex}`.")

    tokens.pop(0)
    return {"value": next_token}


def evaluate_sequence(
    grammar: Grammar,
    tokens_manager: TokensManager,
    sequence: list[str]
) -> AstNode:
    mutable_tokens_manager = tokens_manager.copy()
    children: list[AstNode] = []
    for node in sequence:
        ast_node = evaluate_node(grammar, mutable_tokens_manager, node)
        children.append(ast_node)

    tokens_manager.set_tokens(mutable_tokens_manager.tokens)
    return {"children": children}


def evaluate_rule(
    grammar: Grammar,
    tokens_manager: TokensManager,
    rule: dict
) -> AstNode:
    tokens = tokens_manager.tokens
    literal = rule.get("literal")
    if literal is not None:
        ast_node = evaluate_literal(tokens, literal)
        return ast_node
    
    regex = rule.get("regex")
    if regex is not None:
        ast_node = evaluate_regex(tokens, regex)
        return ast_node
    
    sequence = rule.get("sequence")
    if sequence is not None:
        mutable_tokens_manager = tokens_manager.copy()
        ast_node = evaluate_sequence(grammar, mutable_tokens_manager, sequence)
        mutated_tokens = mutable_tokens_manager.tokens
        tokens_manager.set_tokens(mutated_tokens)
        return ast_node

    raise AstParseError(f"Invalid rule: {rule}")


def evaluate_node(
    grammar: Grammar,
    tokens_manager: TokensManager,
    node: str
) -> AstNode:
    rules = grammar.get(node, [])
    if not rules:
        raise AstParseError(
            f"Reached node `{node}`, which has no defined rules."
        )

    error = None
    ast_node = None
    for rule in rules:
        try:
            mutable_tokens_manager = tokens_manager.copy()
            rule_node = evaluate_rule(grammar, mutable_tokens_manager, rule)

            remaining_tokens = mutable_tokens_manager.tokens
            if node == ROOT and remaining_tokens:
                raise AstParseError(
                    "Could not apply `root` rule to remaining tokens: "
                    f"{remaining_tokens}"
                )

            tokens_manager.set_tokens(remaining_tokens)
            ast_node = rule_node
            break
        except Exception as e:
            error = e
            continue

    if not ast_node:
        if error:
            raise error

        remaining_source_sample = SPACE.join(tokens[:3])[:20]
        raise AstParseError(
            f"Failed to parse `{current_node}` at: "
            f"`{remaining_source_sample}`."
        )

    ast_node = {"type": node, **ast_node}
    return ast_node


def parse_ast(grammar: Grammar, source: str) -> AstNode:
    tokens = get_tokens_string_safe(source)
    tokens_manager = TokensManager(tokens)
    root = evaluate_node(grammar, tokens_manager, ROOT)

    remaining_tokens = tokens_manager.tokens
    if remaining_tokens:
        raise AstParseError(
            "Satisfied `root` rule, but unparsed tokens remain: "
            f"{remaining_tokens}"
        )

    children = root.get("children")
    if not children:
        raise AstParseError("Did not parse anything for `root`.")

    n = len(children)
    if n > 1:
        raise AstParseError(f"Parsed {n} nodes for `root`. Expected only one.")

    return children[0]
