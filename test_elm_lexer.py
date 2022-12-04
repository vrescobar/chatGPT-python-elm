import pytest

from elm_lexer import lex


@pytest.mark.parametrize("input_text,expected", [
    (
        "1 + 2",
        [
            ("NUMBER", "1"),
            ("PLUS", "+"),
            ("NUMBER", "2"),
        ],
    ),
])
def test_lexer(input_text, expected):
    assert list(lex(input_text)) == expected
