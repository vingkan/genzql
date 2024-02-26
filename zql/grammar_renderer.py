from zql.grammar import AstNode
from zql.types import SqlQuery


VALUE_NODES: set[str] = {
    "word",
    "integer",
    "quoted_expr",
}
SINGLE_CHILD_PASSTHROUGH_NODES: set[str] = {
    "zql",
    "operator",
    "cond_operator",
    "union_clause",
}
LITERAL_NODES: dict[str, str] = {
    "terminal": ";",
    "comma": ",",
    "dot": ".",
    "alias": "AS",
    "select": "SELECT",
    "from": "FROM",
    "where": "WHERE",
    "limit": "LIMIT",
    "union_all": "UNION ALL",
    "union": "UNION",
    "is": "IS",
    "is_not": "IS NOT",
    "equal": "=",
    "not_equal": "!=",
    "and": "AND",
    "or": "OR",
}


class QueryRenderError(Exception):
    pass


def render_query(ast: AstNode) -> SqlQuery:
    return render_node(ast)


def render_node(ast: AstNode) -> SqlQuery:
    node_type = ast.get("type")
    children = ast.get("children", [])
    if not node_type:
        raise QueryRenderError(f"Node should have a `type`: {ast}")

    if node_type in VALUE_NODES:
        return ast.get("value")

    if node_type in SINGLE_CHILD_PASSTHROUGH_NODES:
        return render_node(children[0])

    literal = LITERAL_NODES.get(node_type)
    if literal is not None:
        return literal

    if node_type == "statement":
        if len(children) > 1:
            raise NotImplementedError("DDL and DML queries not yet supported.")

        return render_node(children[0])

    if node_type == "query_stmt":
        if len(children) == 1:
            return render_node(children[0])

        explain = render_node(children[0])
        query = render_node(children[1])
        return f"{explain} {query}"

    if node_type == "query":
        if len(children) > 1:
            raise NotImplementedError("CTEs not yet supported.")

        return render_node(children[0])

    if node_type == "simple_query":
        select_query_a = render_node(children[0])
        if len(children) == 1:
            return select_query_a

        union = render_node(children[1])
        select_query_b = render_node(children[2])
        return f"{select_query_a}\n{union}\n{select_query_b}"

    if node_type == "select_query":
        select_clause = render_node(children[0])
        if len(children) == 1:
            return select_clause

        from_query = render_node(children[1])
        return f"{select_clause}\n{from_query}"

    if node_type == "select_clause":
        select = render_node(children[0])
        select_expr_list = render_node(children[1])
        return f"{select} {select_expr_list}"

    if node_type == "select_expr_list":
        select_expr = render_node(children[0])
        if len(children) == 1:
            return select_expr

        comma = render_node(children[1])
        select_expr_list = render_node(children[2])
        return f"{select_expr}{comma} {select_expr_list}"

    if node_type == "select_expr":
        expression = render_node(children[0])
        if len(children) == 1:
            return expression

        alias = render_node(children[1])
        expression_alias = render_node(children[2])
        return f"{expression} {alias} {expression_alias}"

    if node_type == "expression":
        expr_a = render_node(children[0])
        if len(children) == 1:
            return expr_a

        operator = render_node(children[1])
        expr_b = render_node(children[2])
        return f"{expr_a} {operator} {expr_b}"

    if node_type == "single_expr":
        first_child = children[0]
        expr_type = first_child.get("type")
        supported_expression_types = {"word", "integer", "float", "quoted_expr"}
        if expr_type not in supported_expression_types:
            raise NotImplementedError(
                f"Expression type `{expr_type}` not yet supported"
            )

        return render_node(first_child)

    if node_type == "from_query":
        if len(children) == 1:
            return render_node(children[0])

        from_clause = render_node(children[0])
        where_query = render_node(children[1])
        return f"{from_clause}\n{where_query}"

    if node_type == "from_clause":
        if len(children) > 2:
            raise NotImplementedError("JOIN not yet supported.")

        from_literal = render_node(children[0])
        table = render_node(children[1])
        return f"{from_literal} {table}"

    if node_type == "table":
        first_child = children[0]
        if first_child.get("type") != "table_name":
            raise NotImplementedError("Subquery not yet supported.")

        return render_node(first_child)

    if node_type == "table_name":
        table_name_word = render_node(children[0])
        if len(children) == 1:
            return table_name_word

        alias = render_node(children[1])
        table_name_alias = render_node(children[2])
        return f"{table_name_word} {alias} {table_name_alias}"

    if node_type == "where_query":
        if len(children) == 1:
            return render_node(children[0])

        where_query = render_node(children[0])
        groupby_query = render_node(children[1])
        return f"{where_query}\n{groupby_query}"

    if node_type == "where_clause":
        where = render_node(children[0])
        condition_list = render_node(children[1])
        return f"{where} {condition_list}"

    if node_type == "condition_list":
        expr_a = render_node(children[0])
        if len(children) == 1:
            return expr_a

        cond_operator = render_node(children[1])
        expr_b = render_node(children[2])
        return f"{expr_a}\n{cond_operator} {expr_b}"

    if node_type == "groupby_query":
        if len(children) == 1:
            return render_node(children[0])

        groupby_query = render_node(children[0])
        having_query = render_node(children[1])
        return f"{groupby_query}\n{having_query}"

    if node_type == "having_query":
        if len(children) == 1:
            return render_node(children[0])

        having_query = render_node(children[0])
        orderby_query = render_node(children[1])
        return f"{having_query}\n{orderby_query}"

    if node_type == "orderby_query":
        if len(children) == 1:
            return render_node(children[0])

        orderby_query = render_node(children[0])
        limit_clause = render_node(children[1])
        return f"{orderby_query}\n{limit_clause}"

    if node_type == "limit_query":
        if len(children) == 1:
            return render_node(children[0])

        limit_clause = render_node(children[0])
        union_query = render_node(children[1])
        return f"{limit_clause}\n{union_query}"

    if node_type == "union_query":
        if len(children) == 1:
            return render_node(children[0])

        union_clause = render_node(children[0])
        simple_query = render_node(children[1])
        return f"{union_clause}\n{simple_query}"

    if node_type == "limit_clause":
        limit = render_node(children[0])
        limit_amount = render_node(children[1])
        return f"{limit} {limit_amount}"

    if node_type == "limit_amount":
        return render_node(children[0])

    if node_type == "float":
        whole = render_node(children[0])
        dot = render_node(children[1])
        decimal = render_node(children[2])
        return f"{whole}{dot}{decimal}"

    raise NotImplementedError(f"Node type `{node_type}` not yet supported.")
