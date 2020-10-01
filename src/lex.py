import ply.lex as lex
import sys


class LineCounter:
    def __init__(self):
        self.prev_line = 1
        self.prev_tok = 0
        self.last_line_tok = 0
        self.col = 0
        self.no_error = True

    def reset(self):
        self.prev_line = 1
        self.prev_tok = 0
        self.last_line_tok = 0
        self.col = 0
        self.no_error = True

    def update_pos(self, token):
        if token.lineno != self.prev_line:
            self.prev_line = token.lineno
            self.last_line_tok = self.prev_tok
        self.prev_tok = token.lexpos + len(str(token.value))
        token.lexpos -= self.last_line_tok


counter = LineCounter()

reserved = {
    'module': 'MODULE',
    'sig': 'SIG',
    'type': 'TYPE'
}

tokens = [
             'ID',
             'OP',
             'OR',
             'AND',
             'OBR',
             'CBR',
             'POINT'
         ] + list(reserved.values())

t_OP = r':-'

t_OBR = r'\('
t_CBR = r'\)'

t_AND = r'\,'
t_OR = r'\;'
t_POINT = r'\.'


def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'ID')
    return t


t_ignore = ' \t'


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)
    counter.update_pos(t)


def t_error(t):
    counter.update_pos(t)
    counter.no_error = False
    print("Illegal character '%s' at line %i at pos %i" % (t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)


lexer = lex.lex()


def _s_get_tokes(string):
    str_tokens = []
    lexer.input(string)
    while True:
        tok = lexer.token()
        if not tok:
            break
        counter.update_pos(tok)
        str_tokens.append(tok)
    errors = counter.no_error
    counter.reset()
    return errors, str_tokens


def get_tokes(filename, is_file=True):
    if not is_file:
        return _s_get_tokes(filename)
    file_tokens = []
    with open(filename) as f:
        lexer.input(f.read())
        while True:
            tok = lexer.token()
            if not tok:
                break
            counter.update_pos(tok)
            file_tokens.append(tok)
    errors = counter.no_error
    counter.reset()
    return errors, file_tokens


if __name__ == "__main__":
    with open(sys.argv[1]) as mf:
        lexer.input(mf.read())
        while True:
            mtok = lexer.token()
            if not mtok:
                break
            counter.update_pos(mtok)
            print(mtok)
