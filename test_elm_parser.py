import pytest

from elm_parser import parse
from elm_types import (
    Program,
    Expr,
    Literal,
    Ident,
    Tuple,
    List_,
    Record,
    Field,
    BinOp,
    UnOp,
    Let,
    LetRec,
    Match,
    Lambda,
    FunctionCall,
)


@pytest.mark.parametrize("input_text,expected", [
    (
        "1 + 2",
        Program(
            [
                Expr(
                    BinOp(
                        Literal(1),
                        "+",
                        Literal(2)
                    )
                )
            ]
        ),
    ),
])
def test_parser(input_text, expected):
    assert parse(input_text) == expected
