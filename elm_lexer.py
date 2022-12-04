import ply.lex as lex

# List of token names. This is always required
tokens = (
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "MOD",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "LT",
    "GT",
    "EQ",
    "INTEGER",
    "FLOAT",
    "STRING",
    "LET",
    "REC",
    "DEFINE",
    "IN",
    "MATCH",
    "WITH",
    "BAR",
    "ARROW",
    "LAMBDA",
    # "MINUS",
    "UMINUS"
    "NOT",
    "IDENT",
    "COMMA",
    "COLON",
)

# Regular expression rules for simple tokens
t_ADD = r"\+"
t_SUB = r"-"
t_MUL = r"\*"
t_DIV = r"/"
t_MOD = r"%"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LT = r"<"
t_GT = r">"
t_EQ = r"="
t_LET = r"let"
t_REC = r"rec"
t_DEFINE = r"="
t_IN = r"in"
t_MATCH = r"match"
t_WITH = r"with"
t_BAR = r"\|"
t_ARROW = r"->"
t_LAMBDA = r"\\"
# t_MINUS = r"\-"
# t_NOT = r"!"


# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"

# Define a rule for the UMINUS token
def t_UMINUS(t):
    r'-'
    # If the next token is a number, return a UMINUS token
    if t.lexer.peek() in "0123456789":
        return t


def t_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = str(t.value)
    return t


def t_IDENT(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    return t


def t_COMMA(t):
    r","
    return t


def t_COLON(t):
    r":"
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
