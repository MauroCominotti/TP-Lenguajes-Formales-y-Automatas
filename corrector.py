import os
import sys
import importlib

files = os.listdir('.')
module_file = [f.split('.')[0] for f in files if 'grupo' in f][0]

grupo = importlib.import_module(module_file)

samples = [
    ##############################################################################
    # Testing SELECT, FROM
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT c.first_name, c.last_name 
        FROM customers AS c
        ''',
        {'customers': ['first_name', 'last_name']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, GROUP BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        GROUP BY customers.first_name, customers.last_name
        ''',
        {'customers': ['first_name', 'id', 'last_name']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, GROUP BY, ORDER BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        GROUP BY customers.first_name, customers.last_name
        ORDER BY customers.edad ASC, customers.pais
        ''',
        {'customers': ['first_name', 'id', 'last_name']}
    ),

    ##############################################################################
    # Testing SELECT, FROM - AS, WHERE
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT c.first_name, c.last_name
        FROM customers AS c
        WHERE c.id = 2
        ''',
        {'customers': ['first_name', 'id', 'last_name']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, WHERE
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        WHERE customers.id = 2
        ''',
        {'customers': ['first_name', 'id', 'last_name']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, WHERE, GROUP BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        WHERE customers.id = 2
        GROUP BY customers.first_name, customers.last_name
        ''',
        {'customers': ['first_name', 'id', 'last_name']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, WHERE, GROUP BY, ORDER BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        WHERE customers.id = 2
        GROUP BY customers.first_name, customers.last_name
        ORDER BY customers.edad ASC, customers.pais
        ''',
        {'customers': ['edad', 'first_name', 'id', 'last_name', 'pais']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, WHERE, GROUP BY, HAVING
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        WHERE customers.id = 2
        GROUP BY customers.first_name, customers.last_name
        HAVING customers.edad > 18
        ''',
        {'customers': ['edad', 'first_name', 'id', 'last_name', 'pais']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        WHERE customers.id = 2
        GROUP BY customers.first_name, customers.last_name
        HAVING customers.edad > 18
        ORDER BY customers.edad ASC, customers.pais
        ''',
        {'customers': ['edad', 'first_name', 'id', 'last_name', 'pais']}
    ),


    ##############################################################################
    ##################################  JOINS  ###################################
    ##############################################################################

    ##############################################################################
    # Testing SELECT, FROM, LEFT JOIN
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT c.first_name, c.last_name, p.number 
        FROM customers AS c
        LEFT JOIN phones_numbers AS p ON c.id = p.customer_id 
        ''',
        {'customers': ['first_name', 'id', 'last_name'],
         'phones_numbers': ['customer_id', 'number']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, LEFT JOIN, GROUP BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        LEFT JOIN phones_numbers AS p ON c.id = p.customer_id 
        GROUP BY customers.first_name, customers.last_name
        ''',
        {'customers': ['first_name', 'id', 'last_name'],
         'phones_numbers': ['customer_id', 'number']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, LEFT JOIN, GROUP BY, ORDER BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        LEFT JOIN phones_numbers AS p ON c.id = p.customer_id 
        GROUP BY customers.first_name, customers.last_name
        ORDER BY customers.edad ASC, customers.pais
        ''',
        {'customers': ['edad', 'first_name', 'id', 'last_name', 'pais'],
         'phones_numbers': ['customer_id', 'number']}
    ),












    ##############################################################################
    # Testing SELECT, DISTINCT, FROM - AS, LEFT JOIN - AS - ON
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT DISTINCT c.first_name, c.last_name, p.number
        FROM customers AS c
        LEFT JOIN phones_numbers AS p ON c.id = p.customer_id 
        ''',
        {'customers': ['first_name', 'id', 'last_name'],
         'phones_numbers': ['customer_id', 'number']}
    ),

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM - AS, INNER JOIN - AS - ON
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT DISTINCT c.first_name, c.last_name, p.number
        FROM customers AS c
        INNER JOIN phones_numbers AS p ON c.id = p.customer_id 
        ''',
        {'customers': ['first_name', 'id', 'last_name'],
         'phones_numbers': ['customer_id', 'number']}
    ),

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM - AS, LEFT JOIN - ON
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT DISTINCT c.first_name, c.last_name, phones_numbers.number
        FROM customers AS c
        LEFT JOIN phones_numbers ON c.id = phones_numbers.customer_id 
        ''',
        {'customers': ['first_name', 'id', 'last_name'],
         'phones_numbers': ['customer_id', 'number']}
    ),

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM, LEFT JOIN - ON
    # Testing that the table names are without an alias, and same field for
    # both tables
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT DISTINCT customers.first_name, customers.last_name, phones_numbers.number
        FROM customers
        INNER JOIN phones_numbers ON customers.id = phones_numbers.customer_id AND customers.phone = phones_numbers.phone
        ''',
        {'customers': ['first_name', 'id', 'last_name', 'phone'],
         'phones_numbers': ['customer_id', 'number', 'phone']}
    ),

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM, LEFT JOIN - ON, WHERE
    # Testing that the table names are without an alias
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT DISTINCT customers.first_name, customers.last_name, phones_numbers.number
        FROM customers
        INNER JOIN phones_numbers ON customers.id = phones_numbers.customer_id AND customers.phone = phones_numbers.phone
        WHERE customers.id > 10
        ''',
        {'customers': ['first_name', 'id', 'last_name', 'phone'],
         'phones_numbers': ['customer_id', 'number', 'phone']}
    ),

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM, LEFT JOIN - ON, WHERE, GROUP BY
    # Testing that the table names are without an alias
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT DISTINCT customers.pais, customers.edad, phones_numbers.prefijo
        FROM customers
        INNER JOIN phones_numbers ON customers.id = phones_numbers.customer_id AND customers.phone = phones_numbers.phone
        WHERE customers.id > 10
        GROUP BY customers.pais, customers.edad, phones_numbers.prefijo
        ''',
        {'customers': ['edad', 'id', 'pais', 'phone'],
         'phones_numbers': ['customer_id', 'phone', 'prefijo']}
    ),

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM - AS, LEFT JOIN - ON, WHERE, GROUP BY, ORDER BY
    # Testing that the table names are without an alias
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT DISTINCT customers.pais, c.edad, phones_numbers.prefijo
        FROM customers AS c
        INNER JOIN phones_numbers ON c.id = phones_numbers.customer_id AND c.phone = phones_numbers.phone
        WHERE c.id > 10
        GROUP BY c.pais, c.edad, phones_numbers.prefijo
        ORDER BY c.edad ASC, c.pais
        ''',
        {'customers': ['edad', 'id', 'pais', 'phone'],
         'phones_numbers': ['customer_id', 'phone', 'prefijo']}
    ),

    ##############################################################################
    ##################################  ERRORS  ##################################
    ##############################################################################

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM, INNER JOIN - ON
    # Testing that the table name it's not with an alias and the fields are
    # with an undefined alias
    ##############################################################################
    (   # Should throw error
        '''
        SELECT DISTINCT c.first_name, c.last_name, p.number
        FROM customers
        INNER JOIN phones_numbers AS p ON c.id = p.customer_id 
        ''',
        {"Error"}
    ),

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM - AS, INNER JOIN - ON
    # Testing that the table name it's with an alias and the fields after 'ON'
    # are with an undefined alias
    ##############################################################################
    (
        # Should throw error
        '''
        SELECT DISTINCT c.first_name, c.last_name, p.number
        FROM customers AS c
        INNER JOIN phones_numbers AS p ON q.id = p.customer_id AND r.phone = p.phone
        ''',
        {"Error"}
    ),

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM - AS, INNER JOIN - ON
    # Testing that the table name it's with an alias and the fields on 'SELECT'
    # are with an undefined alias
    ##############################################################################
    (
        # Should throw error
        '''
        SELECT DISTINCT q.first_name, r.last_name, s.number
        FROM customers AS c
        INNER JOIN phones_numbers AS p ON c.id = p.customer_id AND c.phone = p.phone
        ''',
        {"Error"}
    ),

    ##############################################################################
    # Testing SELECT, DISTINCT, FROM - AS, INNER JOIN - ON
    # Testing that the table name it's with an alias and the fields on 'SELECT'
    # are with an undefined alias
    ##############################################################################
    (
        # Should throw error
        '''
        SELECT DISTINCT q.first_name, r.last_name, s.number
        FROM customers AS c
        INNER JOIN phones_numbers AS p ON c.id = p.customer_id AND c.phone = p.phone
        ''',
        {"Error"}
    ),
]

for ix, sample in enumerate(samples):
    print('***** Resultados test parsing ejemplo {} *****'.format(ix+1))
    print(sample[0])
    print('-' * 3, ' Fin consulta ', '-' * 3)

    try:
        result = grupo.parse_select_statement(sample[0])

        if result != sample[1]:
            resultStr = 'incorrecto'
        else:
            resultStr = 'correcto'

        print()
        print('El resultado de la comprobación fue {} !'.format(resultStr))
        print('Resultado entregado: ', result)
        print('Resultado esperado: ', sample[1])

    except Exception as e:
        print('''Se produjo una excepción al intentar parsear el ejemplo y/o 
                 comprobar el resultado !''')
        print(e)
    print('')
