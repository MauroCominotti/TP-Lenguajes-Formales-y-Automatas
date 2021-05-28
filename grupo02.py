import ply.lex as lex

tokens = [
    'ID',
    'NUMBER',
    'LPAREN',  # Parentesis que abre
    'RPAREN',  # Parentesis que cierra
    'COMMA',  # Coma
    'SEMMICOLOM',  # Punto y Coma
    'DOT',  # Punto
    'EQ',  # Comprueba que 2 expresiones son iguales
    'NE',  # Comprueba que 2 expresiones no son iguales
    'LT',  # Comprueba que la expresión de la izquierda es menor que la expresión de la derecha
    'LTE',  # Comprueba que la expresión de la izquierda es menor o igual que la expresión de la derecha
    'GT',  # Comprueba que la expresión de la izquierda es mayor que la expresión de la derecha
    'GTE'  # Comprueba que la expresión de la izquierda es mayor o igual que la expresión de la derecha
]

reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'on': 'ON',
    'as': 'AS',
    'group by': 'GROUP_BY',
    'inner join': 'INNER_JOIN',
    'left join': 'LEFT_JOIN',
    'in': 'IN',
    'oder by': 'ORDER_BY',
    'having': 'HAVING'
}

tokens = tokens + list(reserved.values())


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
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
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMMICOLOM = r';'
t_DOT = r'\.'
t_EQ = r'='
t_NE = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'>='

# Build the lexer
lexer = lex.lex()

# data = 'select P.apellido as perro, P.nombre from persona as P'
# lexer.input(data)

# while True:
#     token = lexer.token()
#     if not token:
#         break
#     print(token)


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
