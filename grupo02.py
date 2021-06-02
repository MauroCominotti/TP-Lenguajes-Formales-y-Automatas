import ply.lex as lex
import ply.yacc as yacc

diccionario_tablas = {}
diccionario_columnas = {}

tokens = [
    'ID',
    'NUMERO',
    'PAREN_IZQ',  # '('
    'PAREN_DER',  # ')'
    'COMA',  # ','
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
    'INNER': 'INNER',
    'JOIN': 'JOIN',
    'LEFT': 'LEFT',
    'GROUP': 'GROUP',
    'ORDER': 'ORDER',
    'BY': 'BY',
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
    '0': 'TRUE',
    '1': 'FALSE'
}

tokens = tokens + list(reserved.values())


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMERO(t):
    r'\d+'  # El mas indica 1 o mas veces
    t.type = reserved.get(t.value, 'NUMERO')

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


def p_query(p):
    '''query : SELECT columnas FROM tablas
             | SELECT columnas FROM tablas WHERE condiciones
             | SELECT columnas FROM tablas WHERE condiciones GROUP BY columnas_group_by
             | SELECT columnas FROM tablas WHERE condiciones GROUP BY columnas_group_by HAVING condicion_having
             | SELECT columnas FROM tablas WHERE condiciones GROUP BY columnas_group_by HAVING condicion_having ORDER BY columnas_order_by
             | SELECT columnas FROM tablas joins WHERE condiciones
             | SELECT columnas FROM tablas joins WHERE condiciones GROUP BY columnas_group_by
             | SELECT columnas FROM tablas joins WHERE condiciones GROUP BY columnas_group_by HAVING condicion_having
             | SELECT columnas FROM tablas joins WHERE condiciones GROUP BY columnas_group_by HAVING condicion_having ORDER BY columnas_order_by'''


def p_columnas(p):
    '''columnas : columna
                | columna COMA columnas'''


def p_columna(p):
    '''columna : ID PUNTO ID
               | ID PUNTO ID AS COMILLA ID COMILLA
               | DISTINCT ID PUNTO ID 
               | DISTINCT ID PUNTO ID AS COMILLA ID COMILLA'''
    key = p[1] if p[1] != 'DISTINCT' else p[2]
    if len(p) == 4 or len(p) == 5:
        column1 = p[3] if p[1] != 'DISTINCT' else p[4]
        if key in diccionario_columnas:
            if column1 not in diccionario_columnas[key]:
                # Actualizo registro existente si no está en el array
                diccionario_columnas[key].append(column1)
        else:
            # Creo un nuevo registro ya que no existe
            diccionario_columnas[key] = [column1]
    # TODO > Por que tengo que guardar el alias de la columna????? Tenemos que imprimir el alias?
    # else:
    #     column2 = p[6] if p[1] != 'DISTINCT' else p[7]
    #     if key in diccionario_columnas:
    #         # Actualizo registro existente
    #         diccionario_columnas[key].append(column2)
    #     else:
    #         # Creo un nuevo registro ya que no existe
    #         diccionario_columnas[key] = [column2]


def p_tablas(p):
    '''tablas : tabla
              | tabla COMA tablas'''


def p_tabla(p):
    '''tabla : ID AS ID
             | ID ID
             | ID'''
    if len(p) == 3:
        alias_tabla = p[2]
    else:
        if len(p) == 4:
            alias_tabla = p[3]
        else:
            # Puede venir sola la tabla?
            alias_tabla = 'None'

    nombre_tabla = p[1]
    diccionario_tablas.setdefault(nombre_tabla, alias_tabla)


def p_joins(p):
    '''joins : INNER JOIN tabla ON condiciones
             | LEFT JOIN tabla ON condiciones'''


def p_condiciones(p):
    '''condiciones : condicion
                   | ID PUNTO ID subconsulta
                   | condiciones AND condiciones
                   | condiciones OR condiciones
                   | PAREN_IZQ condiciones OR condiciones PAREN_DER'''


def p_condicion(p):
    '''condicion : ID PUNTO ID signo valor
                 | ID PUNTO ID signo ID PUNTO ID
                 | ID PUNTO ID nulleable
                 | ID PUNTO ID IGUAL booleano'''
    key = p[1]
    column1 = p[3]
    if key in diccionario_columnas:
        if column1 not in diccionario_columnas[key]:
            # Actualizo registro existente si no está en el array
            diccionario_columnas[key].append(column1)
    else:
        # Creo un nuevo registro ya que no existe
        diccionario_columnas[key] = [column1]
    if len(p) == 8:
        key = p[5]
        column2 = p[7]
        if key in diccionario_columnas:
            if column2 not in diccionario_columnas[key]:
                # Actualizo registro existente si no está en el array
                diccionario_columnas[key].append(column2)
        else:
            # Creo un nuevo registro ya que no existe
            diccionario_columnas[key] = [column2]

def p_signo(p):
    '''signo : MENOR_IZQ 
             | MAYOR_IZQ 
             | MEN_IGUAL_IZQ 
             | MAY_IGUAL_IZQ 
             | IGUAL 
             | DESIGUAL'''


def p_valor(p):
    '''valor : ID 
             | NUMERO'''


def p_nulleable(p):
    '''nulleable : NULL
                 | IS NOT NULL'''


def p_booleano(p):
    '''booleano : TRUE
                | FALSE'''


def p_subconsulta(p):
    '''subconsulta : IN PAREN_IZQ query PAREN_DER
                   | NOT IN PAREN_IZQ query PAREN_DER'''


# if p[1] == 'as':
#     print(p[1], p[2])

def p_columnas_group_by(p):
    '''columnas_group_by : ID PUNTO ID
                         | ID PUNTO ID COMA columnas_group_by'''


def p_columnas_order_by(p):
    '''columnas_order_by : ID PUNTO ID orden
                         | ID PUNTO ID orden COMA columnas_order_by'''


def p_orden(p):
    '''orden : ASC
             | DESC'''


def p_condicion_having(p):
    '''condicion_having : func_resumen signo valor
                        | func_resumen signo func_resumen'''


def p_func_resumen(p):
    '''func_resumen : MIN PAREN_IZQ ID PUNTO ID PAREN_DER
                    | MAX PAREN_IZQ ID PUNTO ID PAREN_DER
                    | COUNT PAREN_IZQ ID PUNTO ID PAREN_DER
                    | COUNT PAREN_IZQ DISTINCT ID PUNTO ID PAREN_DER'''


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


def parse_select_statement(s):
    diccionario_final = {}
    yacc.yacc()
    yacc.parse(s)
    for z, y in diccionario_tablas.items():
        if y in diccionario_columnas.keys():
            diccionario_final.setdefault(z, diccionario_columnas[y])
            diccionario_final[z] = sorted(diccionario_final.get(z))
    return diccionario_final


# If you want to test it in local just descomment this
if __name__ == '__main__':
    parser = yacc.yacc()
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        yacc.parse(s)
        result = parse_select_statement(s)
        print(result)




