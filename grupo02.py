import ply.lex as lex

diccionario_tablas = {}
diccionario_columnas = {}

tokens = [
    'ID',
    'NUMERO',
    'PAREN_IZQ',  # '('
    'PAREN_DER',  # ')'
    'COMA',  # ','
    'PUNTOCOMA',  # ';'
    'PUNTO',  # '.'
    'COMILLA',  # ' " '
    'IGUAL',  # '='
    'DESIGUAL',  # '<>'
    'MENOR_IZQ',  # '<'
    'MEN_IGUAL_IZQ',  # '<='
    'MAYOR_IZQ',  # '>'
    'MAY_IGUAL_IZQ'  # '>='
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
    'NULL': 'NULL',
    'NOT': 'NOT',
    'IS': 'IS',
    'ASC': 'ASC',
    'DESC': 'DESC',
    'TRUE': 'TRUE',
    'FALSE': 'FALSE'
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
t_COMILLA = r'"'
t_IGUAL = r'='
t_DESIGUAL = r'<>'
t_MENOR_IZQ = r'<'
t_MEN_IGUAL_IZQ = r'<='
t_MAYOR_IZQ = r'>'
t_MAY_IGUAL_IZQ = r'>='

# Build the lexer
lexer = lex.lex()


# data = 'select P.apellido as perro, P.nombre from persona as P, WHERE count max min and or'
# lexer.input(data)

# while True:
#     token = lexer.token()
#     if not token:
#         break
#     print(token)

def p_query(p):
    '''query : SELECT columnas FROM tablas
             | SELECT columnas FROM tablas WHERE condicion'''


def p_columnas(p):
    '''columnas : columna
                   | columna COMA columna'''


def p_columna_con_tabla_antepuesta(p):
    '''columna : ID PUNTO ID
               | ID PUNTO ID AS ID'''
    if len(p) == 4:
        print("p_columna_con_tabla_antepuesta   ", p[1], p[2], p[3])
    else:
        print("p_columna_con_tabla_antepuesta   ", p[1], p[2], p[3], p[4])

        #    if diccionario_columnas is None:
    diccionario_columnas.setdefault(p[1], p[3])

    # diccionario_columnas[p[1]] = [ p[3] ]
    #  else:
    # diccionario_columnas[p[1]].append(p[3])
    print("DICCIONARIO COLUMNA 1", diccionario_columnas)
    print("DICCIONARIO TABLA 1", diccionario_tablas)


#   for elemento in diccionario_tablas:
#        print(diccionario_tablas)

#    for x, y in enumerate(diccionario_tablas):
#       print("DICCIONARIO", x, y)

# list(filter((lambda x: x[0] == p[1]), range(diccionario_tablas)))


def p_tablas(p):
    '''tablas : tabla
              | tabla COMA tabla'''


def p_tabla_con_alias(p):
    '''tabla : ID AS ID
             | ID ID'''
    if len(p) == 3:
        print("p_tabla_con_alias   ", p[1], p[2])
        alias_tabla = p[2]

    else:
        print("p_tabla_con_alias   ", p[1], p[2], p[3])
        alias_tabla = p[3]

    nombre_tabla = p[1]
    diccionario_tablas.setdefault((nombre_tabla, alias_tabla), {})
    print("DICCIONARIO COLUMNA 2", diccionario_columnas)
    print("DICCIONARIO TABLA 2", diccionario_tablas)

    for x, y in diccionario_tablas:
        if y == alias_tabla:
            diccionario_tablas[(x, y)] = diccionario_columnas[alias_tabla]
        print("NUEVO DICCIONARIO TABLAS: ", diccionario_tablas)


def p_condicion(p):
    '''condicion : columnas IGUAL columnas'''


# if p[1] == 'as':
#     print(p[1], p[2])


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
