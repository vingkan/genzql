import pytest
from zql.main import Zql


def test_simple_select_query():
    raw_query = """
    its giving a, b
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b
FROM example
;
    """.strip()
    assert actual == expected


def test_simple_select_query_with_limit():
    raw_query = """
    its giving a, b
    yass example
    say less 10
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b
FROM example
LIMIT 10
;
    """.strip()
    assert actual == expected


def test_select_integer_without_from():
    raw_query = """
    its giving 6
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT 6
;
    """.strip()
    assert actual == expected


def test_select_float_without_from():
    raw_query = """
    its giving 6.04
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT 6.04
;
    """.strip()
    assert actual == expected


def test_select_without_from_string_expression_single_quotes():
    raw_query = """
    its giving 'hello'
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT 'hello'
;
    """.strip()
    assert actual == expected


def test_select_without_from_string_expression_double_quotes():
    raw_query = """
    its giving "hello"
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT "hello"
;
    """.strip()
    assert actual == expected


def test_single_where():
    raw_query = """
    its giving a
    yass example
    tfw a be b
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a
FROM example
WHERE a = b
;
    """.strip()
    assert actual == expected


def test_multi_where_and():
    raw_query = """
    its giving a
    yass example
    tfw a be b
    fax a sike c
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a
FROM example
WHERE a = b
AND a != c
;
    """.strip()
    assert actual == expected


def test_multi_where_or():
    raw_query = """
    its giving a
    yass example
    tfw a be b
    uh a sike c
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a
FROM example
WHERE a = b
OR a != c
;
    """.strip()
    assert actual == expected


def test_multi_where_and_or():
    raw_query = """
    its giving a
    yass example
    tfw a be b
    fax a sike c
    uh b be c
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a
FROM example
WHERE a = b
AND a != c
OR b = c
;
    """.strip()
    assert actual == expected


def test_single_where_string_expression():
    raw_query = """
    its giving a
    yass example
    tfw a be 'ahh'
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a
FROM example
WHERE a = 'ahh'
;
    """.strip()
    assert actual == expected


def test_select_star_short_sheesh():
    raw_query = """
    its giving sheesh
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT *
FROM example
;
    """.strip()
    assert actual == expected


def test_select_star_long_sheesh():
    raw_query = """
    its giving sheeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeesh
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT *
FROM example
;
    """.strip()
    assert actual == expected


def test_select_distinct():
    raw_query = """
    its giving real ones a, b, c
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT DISTINCT a, b, c
FROM example
;
    """.strip()
    assert actual == expected


def test_select_math_expressions():
    raw_query = """
    its giving a, b + c, d * e, f/g, h-i
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b + c, d * e, f / g, h - i
FROM example
;
    """.strip()
    assert actual == expected


def test_select_column_alias():
    raw_query = """
    its giving a, b be flower
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b AS flower
FROM example
;
    """.strip()
    assert actual == expected


def test_select_expression_alias():
    raw_query = """
    its giving a, (b be c) be is_equal
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b = c AS is_equal
FROM example
;
    """.strip()
    assert actual == expected


def test_select_multiple_aliases():
    raw_query = """
    its giving
        a be x,
        b,
        (c + d) be yo,
        e
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a AS x, b, c + d AS yo, e
FROM example
;
    """.strip()
    assert actual == expected


def test_select_postfix_alias():
    raw_query = """
    its giving a, b af be total_b
    yass example
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, SUM(b) AS total_b
FROM example
;
    """.strip()
    assert actual == expected


def test_respect_case():
    raw_query = """
    ITS GIVING a
    yASs example
    tfw a be "hELlO"
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a
FROM example
WHERE a = "hELlO"
;
    """.strip()
    assert actual == expected


def test_single_line_comments():
    raw_query = """
    -- yo wassup its zql
    its giving a, b, c
    yass example
    -- you cappin if you forget this
    no cap
    """
    actual = Zql().parse(raw_query)
#     expected = """
# -- yo wassup its zql
# SELECT a, b, c
# FROM example
# -- you cappin if you forget this
# ;
#     """.strip()
    expected = """
SELECT a, b, c
FROM example
;
    """.strip()
    assert actual == expected


def test_inline_comments():
    raw_query = """
    its giving a, b, c -- yo wassup its zql
    yass example
    no cap -- you cappin if you forget this
    """
    actual = Zql().parse(raw_query)
#     expected = """
# SELECT a, b, c -- yo wassup its zql
# FROM example
# ; -- you cappin if you forget this
#     """.strip()
    expected = """
SELECT a, b, c
FROM example
;
    """.strip()
    assert actual == expected


def test_multiline_comments():
    raw_query = """
    /*
     * yo wassup its zql
     */
    its giving a, b, c
    yass example
    no cap
    /*
    you cappin if you forget this
     */
    """
    actual = Zql().parse(raw_query)
#     expected = """
# /*
# * yo wassup its zql
# */
# SELECT a, b, c
# FROM example
# ;
# /*
# you cappin if you forget this
# */
#     """.strip()
    expected = """
SELECT a, b, c
FROM example
;
    """.strip()
    assert actual == expected


def test_simple_select_union():
    raw_query = """
    its giving a, b, c
    with the bois
    its giving a, b, c
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b, c
UNION
SELECT a, b, c
;
    """.strip()
    assert actual == expected


def test_simple_select_union_all():
    raw_query = """
    its giving a, b, c
    with all the bois
    its giving a, b, c
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b, c
UNION ALL
SELECT a, b, c
;
    """.strip()
    assert actual == expected


def test_select_where_union():
    raw_query = """
    its giving a, b, c
    tfw x be 100
    with the bois
    its giving a, b, c
    tfw y be 100
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b, c
WHERE x = 100
UNION
SELECT a, b, c
WHERE y = 100
;
    """.strip()
    assert actual == expected


def test_select_where_union_all():
    raw_query = """
    its giving a, b, c
    tfw x be 100
    with all the bois
    its giving a, b, c
    tfw y be 100
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b, c
WHERE x = 100
UNION ALL
SELECT a, b, c
WHERE y = 100
;
    """.strip()
    assert actual == expected


def test_join_two_tables():
    raw_query = """
    its giving a, b
    yass table_a
    come through left table_b
    bet a be b
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b
FROM table_a
LEFT JOIN table_b
ON a = b
;
    """.strip()
    assert actual == expected


def test_join_two_tables_explicit_columns():
    raw_query = """
    its giving table_a.a, table_b.b
    yass table_a
    come through left table_b
    bet table_a.a be table_b.b
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT table_a.a, table_b.b
FROM table_a
LEFT JOIN table_b
ON table_a.a = table_b.b
;
    """.strip()
    assert actual == expected


def test_join_two_tables_explicit_columns_explicit_table_aliases():
    raw_query = """
    its giving ta.a, tb.b
    yass table_a be ta
    come through left table_b be tb
    bet ta.a be tb.b
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT ta.a, tb.b
FROM table_a AS ta
LEFT JOIN table_b AS tb
ON ta.a = tb.b
;
    """.strip()
    assert actual == expected


def test_join_two_tables_explicit_columns_implicit_table_aliaes():
    raw_query = """
    its giving ta.a, tb.b
    yass table_a ta
    come through left table_b tb
    bet ta.a be tb.b
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT ta.a, tb.b
FROM table_a ta
LEFT JOIN table_b tb
ON ta.a = tb.b
;
    """.strip()
    assert actual == expected


def test_join_three_tables():
    raw_query = """
    its giving a, b, c
    yass table_a
    come through left table_b
        bet a be b
    come through full outer table_c
        bet a sike c
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b, c
FROM table_a
LEFT JOIN table_b
ON a = b
FULL OUTER JOIN table_c
ON a != c
;
    """.strip()
    assert actual == expected


def test_join_three_tables_multiple_conditions():
    raw_query = """
    its giving a, b, c
    yass table_a
    come through left table_b
        bet a be b
        fax 1 be 1
        uh b sike "quack"
    come through full outer table_c
        bet a sike c
        fax 1 be 1
        uh c sike "quack"
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b, c
FROM table_a
LEFT JOIN table_b
ON a = b
AND 1 = 1
OR b != "quack"
FULL OUTER JOIN table_c
ON a != c
AND 1 = 1
OR c != "quack"
;
    """.strip()
    assert actual == expected


def test_groupby_one_field_simple_aggregation():
    raw_query = """
    its giving a, count(b)
    yass example
    let a cook
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, count(b)
FROM example
GROUP BY a
;
    """.strip()
    assert actual == expected


def test_groupby_one_field_sum_aggregation():
    raw_query = """
    its giving a, b af
    yass example
    let a cook
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, SUM(b)
FROM example
GROUP BY a
;
    """.strip()
    assert actual == expected


def test_groupby_one_field_distinct_aggregation():
    raw_query = """
    its giving a, COUNT(real ones b)
    yass example
    let a cook
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, COUNT(DISTINCT b)
FROM example
GROUP BY a
;
    """.strip()
    assert actual == expected


def test_groupby_multiple_fields():
    raw_query = """
    its giving a, b, c, d, count(e)
    yass example
    let a, b, c, d cook
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b, c, d, count(e)
FROM example
GROUP BY a, b, c, d
;
    """.strip()
    assert actual == expected


def test_groupby_having_with_one_field():
    raw_query = """
    its giving a, count(b)
    yass example
    let a cook
    catch these count(b) bops 10 hands
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, count(b)
FROM example
GROUP BY a
HAVING count(b) > 10
;
    """.strip()
    assert actual == expected


def test_groupby_having_with_multiple_fields():
    raw_query = """
    its giving a, count(b)
    yass example
    let a cook
    catch these
        count(b) bops 10
        fax count(b) kinda flops 100
    hands
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, count(b)
FROM example
GROUP BY a
HAVING count(b) > 10
AND count(b) <= 100
;
    """.strip()
    assert actual == expected


def test_orderby_one_field_desc():
    raw_query = """
    its giving a, b
    yass example
    ngl b high key
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b
FROM example
ORDER BY b DESC
;
    """.strip()
    assert actual == expected


def test_orderby_one_field_asc():
    raw_query = """
    its giving a, b
    yass example
    ngl b low key
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b
FROM example
ORDER BY b ASC
;
    """.strip()
    assert actual == expected


def test_orderby_one_field_nulls_first():
    raw_query = """
    its giving a, b
    yass example
    ngl b high key yikes
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b
FROM example
ORDER BY b NULLS FIRST
;
    """.strip()
    assert actual == expected


def test_orderby_one_field_nulls_last():
    raw_query = """
    its giving a, b
    yass example
    ngl b low key yikes
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b
FROM example
ORDER BY b NULLS LAST
;
    """.strip()
    assert actual == expected


def test_orderby_multiple_fields():
    raw_query = """
    its giving a, b, c, d, e
    yass example
    ngl b high key,
        c low key yikes,
        d high key yikes,
        e low key
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a, b, c, d, e
FROM example
ORDER BY b DESC, c NULLS LAST, d NULLS FIRST, e ASC
;
    """.strip()
    assert actual == expected


def test_common_table_expressions():
    raw_query = """
    perchance my_cte_b be (
        its giving a
        yass example
        tfw b be "BBB"
    ),
    my_cte_c be (
        its giving a
        yass example
        tfw c be "CCC"
    )
    its giving a
    yass my_cte_b
    with the bois
    its giving a
    yass my_cte_c
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
WITH my_cte_b AS (
SELECT a
FROM example
WHERE b = "BBB"
),
my_cte_c AS (
SELECT a
FROM example
WHERE c = "CCC"
)
SELECT a
FROM my_cte_b
UNION
SELECT a
FROM my_cte_c
;
    """.strip()
    assert actual == expected


def test_select_from_sub_query_without_alias():
    raw_query = """
    its giving a
    yass (
        its giving a
        yass example
    )
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a
FROM (
SELECT a
FROM example
)
;
    """.strip()
    assert actual == expected


def test_select_from_sub_query_with_alias():
    raw_query = """
    its giving a
    yass (
        its giving a
        yass example
    ) be sub
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a
FROM (
SELECT a
FROM example
) AS sub
;
    """.strip()
    assert actual == expected


def test_select_from_sub_query_with_implicit_alias():
    raw_query = """
    its giving a
    yass (
        its giving a
        yass example
    ) sub
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
SELECT a
FROM (
SELECT a
FROM example
) sub
;
    """.strip()
    assert actual == expected


def test_create_table():
    raw_query = """
    built different girlie example be (
        a int,
        b float,
        c text
    )
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
CREATE TABLE example(
    a int,
    b float,
    c text
);
    """.strip()
    assert actual == expected


def test_create_table_if_not_exists():
    raw_query = """
    built different girlie example or nah be (
        a int,
        b float,
        c text
    )
    no cap
    """
    actual = Zql().parse(raw_query)
    expected = """
CREATE TABLE IF NOT EXISTS example(
    a int,
    b float,
    c text
);
    """.strip()
    assert actual == expected


def test_create_database():
    raw_query = "built different queen db no cap"
    actual = Zql().parse(raw_query)
    assert actual == "CREATE DATABASE db;"


def test_create_database_if_not_exists():
    raw_query = "built different queen db or nah no cap"
    actual = Zql().parse(raw_query)
    assert actual == "CREATE DATABASE IF NOT EXISTS db;"


def test_drop_database():
    raw_query = "yeet queen db no cap"
    actual = Zql().parse(raw_query)
    assert actual == "DROP DATABASE db;"


def test_drop_database_if_not_exists():
    raw_query = "yeet queen db or nah no cap"
    actual = Zql().parse(raw_query)
    assert actual == "DROP DATABASE IF EXISTS db;"


def test_drop_table():
    raw_query = "yeet girlie example no cap"
    actual = Zql().parse(raw_query)
    assert actual == "DROP TABLE example;"


def test_drop_table_if_not_exists():
    raw_query = "yeet girlie example or nah no cap"
    actual = Zql().parse(raw_query)
    assert actual == "DROP TABLE IF EXISTS example;"


def test_insert():
    raw_query = "pushin p into example (1, \"A\") no cap"
    actual = Zql().parse(raw_query)
    assert actual == "INSERT INTO example VALUES (1, \"A\");"
