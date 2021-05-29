import ply.lex as lex


tokens = [
    'ID',
    'NUMERO',
    'PAREN_IZQ',        # '('
    'PAREN_DER',        # ')'
    'COMA',             # ','
    'PUNTOCOMA',        # ';'
    'PUNTO',            # '.'
    'IGUAL',            # '='
    'DESIGUAL',         # '<>'
    'MENOR_IZQ',        # '<'
    'MEN_IGUAL_IZQ',    # '<='
    'MAYOR_IZQ',        # '>'
    'MAY_IGUAL_IZQ'     # '>='
]

reserved = {
    'SELECT': 'SELECT',
    'FROM': 'FROM',
    'WHERE': 'WHERE',
    'ON': 'ON',
    'IN': 'IN',
    'AS': 'AS',
    'INNER JOIN': 'INNER_JOIN',
    'LEFT JOIN': 'LEFT_JOIN',
    'GROUP BY': 'GROUP_BY',
    'ORDER BY': 'ORDER_BY',
    'HAVING': 'HAVING',
    'MIN': 'MIN',
    'MAX': 'MAX',
    'COUNT': 'COUNT',
    'DISTINCT': 'DISTINCT',
    'AND': 'AND',
    'OR': 'OR',

}

tokens = tokens + list(reserved.values())


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMERO(t):
    r'\d+'  # El mas indica 1 o mas veces
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
# Regular expression rules for simple tokens
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_COMA = r','
t_PUNTOCOMA = r';'
t_PUNTO = r'\.'
t_IGUAL = r'='
t_DESIGUAL = r'<>'
t_MENOR_IZQ = r'<'
t_MEN_IGUAL_IZQ = r'<='
t_MAYOR_IZQ = r'>'
t_MAY_IGUAL_IZQ = r'>='

# Build the lexer
lexer = lex.lex()

data = 'select P.apellido as perro, P.nombre from persona as P, WHERE count max min and or'
lexer.input(data)

while True:
    token = lexer.token()
    if not token:
        break
    print(token)


"""
def p_parse_select_statement(p):
    "expression : SELECT ID FROM ID"
    p[0] = p[1]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


import ply.yacc as yacc

parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
"""