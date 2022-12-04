from collections.abc import MutableSequence


class Program:
    def __init__(self, expressions):
        self.expressions = expressions


class Expr:
    pass


class Literal(Expr):
    def __init__(self, value):
        self.value = value


class Ident(Expr):
    def __init__(self, name):
        self.name = name


class Tuple(Expr, MutableSequence):
    def __init__(self, elements):
        self.elements = elements

    def __getitem__(self, index):
        return self.elements[index]

    def __setitem__(self, index, value):
        self.elements[index] = value

    def __delitem__(self, index):
        del self.elements[index]

    def __len__(self):
        return len(self.elements)

    def insert(self, index, value):
        self.elements.insert(index, value)


class List_(Expr, MutableSequence):
    def __init__(self, elements):
        self.elements = elements

    def __getitem__(self, index):
        return self.elements[index]

    def __setitem__(self, index, value):
        self.elements[index] = value

    def __delitem__(self, index):
        del self.elements[index]

    def __len__(self):
        return len(self.elements)

    def insert(self, index, value):
        self.elements.insert(index, value)


class Record(Expr):
    def __init__(self, fields):
        self.fields = fields


class Field:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class BinOp(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnOp(Expr):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class Let(Expr):
    def __init__(self, names, expressions, body):
        self.names = names
        self.expressions = expressions
        self.body = body


class LetRec(Expr):
    def __init__(self, functions, body):
        self.functions = functions
        self.body = body


class Match(Expr):
    def __init__(self, expr, cases):
        self.expr = expr
        self.cases = cases


class Lambda(Expr):
    def __init__(self, arguments, body):
        self.arguments = arguments
        self.body = body


class FunctionCall(Expr):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments
