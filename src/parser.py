import ply.yacc as yacc
import sys

from lex import tokens


class Node:
    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name


def p_error(p):
    if p is not None:
        print("Illegal character '%s' at line %i at pos %i" %
              (p.value[0], p.lineno, p.lexpos))
    else:
        print("Missing point")
    raise ValueError()


def p_prog(p):
    """prog : oper POINT prog
            | oper POINT """
    if len(p) == 3:
        p[0] = Node(p[1], None, ".")
    else:
        p[0] = Node(p[1], p[3], ".")


def p_oper(p):
    """oper : atom OP disj
            | atom"""
    if len(p) == 4:
        p[0] = Node(p[1], p[3], ":-")
    else:
        p[0] = p[1]


def p_disj(p):
    """disj : conj OR disj
            | conj """
    if len(p) == 4:
        p[0] = Node(p[1], p[3], "OR")
    else:
        p[0] = p[1]


def p_conj(p):
    """conj : expression AND conj
            | expression"""
    if len(p) == 4:
        p[0] = Node(p[1], p[3], "AND")
    else:
        p[0] = p[1]


def p_expr(p):
    """expression : OBR disj CBR
                  | atom"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_atom(p):
    """atom : ID
            | ID seq_atom"""
    if len(p) == 2:
        p[0] = Node(None, None,  "ATOM (ID " + str(p[1]) + ")")
    else:
        p[0] = Node(Node(None, None, "ID " + str(p[1])),
                    p[2], "ATOM")


def p_seq_atom(p):
    """seq_atom : OBR atom CBR
                | OBR atom CBR seq_atom
                | ID
                | ID seq_atom"""
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 5:
        p[0] = Node(p[2], p[4], "atom_in_bracket")
    elif len(p) == 2:
        p[0] = Node(None, None, "ID " + str(p[1]))
    else:
        p[0] = Node(Node(None, None, "ID " + str(p[1])),
                    p[2], "seq")


def pr(node):
    a = ""
    if node.left is not None:
        a += pr(node.left)
    if node.name != "seq" and node.name != "ATOM"\
            and node.name != "atom_in_bracket":
        a += " " + node.name
    a += " "
    if node.name == ".":
        a += '\n'
    if node.right is not None:
        a += pr(node.right)
    if node.name == ".":
        return a
    if node.name != "seq" and node.name != "ATOM"\
            and node.name != "atom_in_bracket":
        return "(" + a + ")"
    if node.name == "ATOM":
        return "ATOM (" + a + ")"
    return a


parser = yacc.yacc()

if __name__ == "__main__":
    with open(sys.argv[1]) as f, open(sys.argv[1] + ".out", "w") as f_out:
        text = f.read()
        try:
            tree = parser.parse(text)
            if tree is not None:
                f_out.write(pr(tree))
        except ValueError:
            print("Failed to parse")
