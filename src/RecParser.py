from lex import *
import sys


class Node:
    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name


class Parser:
    def __init__(self, s):
        self.lex = lexer(s)
        self.current = next(self.lex)
        self.prev_lineno = 1
        self.prev_lexpos = 0

    def accept(self, c):
        if self.current == '\0':
            return False
        if self.current.type == c:
            self.prev_lineno = self.current.lineno
            self.prev_lexpos = self.current.lexpos + len(self.current.value)
            self.current = next(self.lex)
            return True
        return False

    def log_err(self, tok, expected):
        if tok == '\0':
            print("Expected", expected, "but got", "NOTHING", "at line",
                  self.prev_lineno, "col", self.prev_lexpos)
            raise ValueError()
        print("Expected", expected, "but got", tok.type, "at line",
              tok.lineno, "col", tok.lexpos)
        raise ValueError()

    def id(self):
        l = self.current
        if self.accept('ID'):
            return Node(None, None, l.value)
        self.log_err(l, 'ID')
        return None

    def disj(self):
        l = self.conj()
        if self.accept('OR'):
            r = self.disj()
            if r is None:
                l.lexpos += len(l.value)
                self.log_err(l, 'expression')
                return None
            return Node(l, r, "or")
        return l

    def conj(self):
        l = self.expr()
        if self.accept('AND'):
            r = self.conj()
            if r is None:
                l.lexpos += len(l.value)
                self.log_err(l, 'expression')
                return None
            return Node(l, r, "and")
        return l

    def expr(self):
        if self.accept('OBR'):
            r = self.disj()
            if self.accept('CBR'):
                return r
            self.log_err(self.current, 'CBR')
            return None
        return self.id()

    def build(self):
        l = self.id()
        if self.accept('OP'):
            r = self.disj()
            if self.accept('POINT'):
                if r is not None:
                    return Node(l, r, ":-")
            self.log_err(self.current, 'POINT')
            return None
        if self.accept('POINT'):
            return l
        self.log_err(self.current, 'POINT OR OPERATOR')
        return None


def pr(node):
    a = "("
    if node.left is not None:
        a += pr(node.left)
    a += " " + node.name + " "
    if node.right is not None:
        a += pr(node.right)
    a += ')'
    return a


def lexer(s):
    for c in s:
        yield c
    while True:
        yield '\0'


def isCorrect(string, is_file=True):
    no_errors, tokens = get_tokes(string, is_file)

    expression = []
    if not no_errors:
        print("Failed to parse")
        return False
    for token in tokens:
        expression.append(token)
        if token.type == 'POINT':
            try:
                p = Parser(expression)
                tree = p.build()
               # if tree is not None:
              #      print(pr(tree))
            except ValueError:
                print("Failed to parse")
                return False
            expression = []
    if len(expression) > 0:
        print("Expected POINT but got NOTHING at line",
              tokens[-1].lineno, "col", tokens[-1].lexpos + len(tokens[-1].value))
        print("Failed to parse")
        return False
    return True


if __name__ == "__main__":
    if isCorrect(sys.argv[1]):
        print("Correct file")
