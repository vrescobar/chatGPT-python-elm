from elm_lexer import tokens
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

# Grammar
# List of operator precedence rules
# (order matters)
precedence = (
    ('right', 'UMINUS'),
    ('right', 'NOT'),
)


def p_program(p):
    "program : expressions"
    p[0] = Program(p[1])


def p_expressions(p):
    """
    expressions : expressions expression
                | expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_expression_integer(p):
    "expression : INTEGER"
    p[0] = Literal(int(p[1]))


def p_expression_float(p):
    "expression : FLOAT"
    p[0] = Literal(float(p[1]))


def p_expression_string(p):
    "expression : STRING"
    p[0] = Literal(p[1][1:-1])


def p_expression_ident(p):
    "expression : IDENT"
    p[0] = Ident(p[1])


def p_expression_tuple(p):
    "expression : LPAREN tuple_expr RPAREN"
    p[0] = Tuple(p[2])


def p_tuple_expr(p):
    """
    tuple_expr : tuple_expr COMMA expression
               | expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_expression_list(p):
    "expression : LBRACKET list_expr RBRACKET"
    p[0] = List_(p[2])


def p_list_expr(p):
    """
    list_expr : list_expr COMMA expression
              | expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_expression_record(p):
    "expression : LBRACE record_expr RBRACE"
    p[0] = Record(p[2])


def p_record_expr(p):
    """
    record_expr : record_expr COMMA record_field
                | record_field
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_record_field(p):
    "record_field : IDENT COLON expression"
    p[0] = Field(p[1], p[3])


def p_expression_binop(p):
    """
    expression : expression ADD expression
               | expression SUB expression
               | expression MUL expression
               | expression DIV expression
               | expression MOD expression
               | expression LT expression
               | expression GT expression
               | expression EQ expression
    """
    p[0] = BinOp(p[2], p[1], p[3])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = UnOp('not', p[2])

def p_expression_unop(p):
    'expression : UMINUS expression'
    p[0] = UnOp('-', p[2])


def p_expression_let(p):
    "expression : LET ident_list DEFINE expressions IN expression"
    p[0] = Let(p[2], p[4], p[6])


def p_ident_list(p):
    """
    ident_list : ident_list COMMA IDENT
               | IDENT
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_expression_let_rec(p):
    "expression : LET REC ident_expr_list IN expressions"
    p[0] = LetRec(p[3], p[5])


def p_ident_expr_list(p):
    """
    ident_expr_list : ident_expr_list COMMA ident_expr
                    | ident_expr
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_ident_expr(p):
    "ident_expr : IDENT DEFINE expression"
    p[0] = (p[1], p[3])


def p_expression_match(p):
    "expression : MATCH expression WITH match_expr_list"
    p[0] = Match(p[2], p[4])


def p_match_expr_list_single(p):
    "match_expr_list : match_expr"
    p[0] = [p[1]]

def p_match_expr_list_multiple(p):
    "match_expr_list : match_expr_list match_expr"
    p[0] = p[1] + [p[2]]

def p_match_expr(p):
    "match_expr : BAR pattern ARROW expression"
    p[0] = (p[2], p[4])


def p_pattern_literal(p):
    """
    pattern : INTEGER
            | FLOAT
            | STRING
    """
    if p[1][0] == '"':
        p[0] = Literal(p[1][1:-1])
    else:
        p[0] = Literal(int(p[1]))


def p_pattern_ident(p):
    "pattern : IDENT"
    p[0] = Ident(p[1])


def p_pattern_tuple(p):
    "pattern : LPAREN pattern_list RPAREN"
    p[0] = Tuple(p[2])


def p_pattern_list(p):
    """
    pattern_list : pattern_list COMMA pattern
                 | pattern
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_expression_lambda(p):
    "expression : LAMBDA pattern_list ARROW expression"
    p[0] = Lambda(p[2], p[4])


def p_expression_function_call(p):
    "expression : expression LPAREN argument_list RPAREN"
    p[0] = FunctionCall(p[1], p[3])


def p_argument_list(p):
    """
    argument_list : argument_list COMMA expression
                  | expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# Error rule for syntax errors
def p_error(p):
    print(f"Syntax error in input: {p}")


# import yacc: yacc.yacc()
from ply import yacc
from elm_lexer import lexer

def parse(text: str) -> Program:
    
    """Parse a string containing Elm-like code into an AST.

    Args:
        text (str): The string containing the code to parse.

    Returns:
        Program: The AST representation of the code.
    """
    # implement the yacc parser with the tokens, lexer , precedence and grammar
    # defined above
    # use the yacc.parse() method to parse the text
    # return the result
    parser = yacc.yacc()
    return parser.parse(text, lexer=lexer)

# parser = yacc.yacc()
#     return parser(text,
#                     lexer=lexer,
#                     tokenfunc=tokens, 
#                     precedence=precedence,
#                     debug=False,
#                     tracking=True)


