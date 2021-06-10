import importlib
import sys
import os
# pip install colorama
from colorama import init, Fore, Back, Style
init(convert=True)

files = os.listdir('.')
module_file = [f.split('.')[0] for f in files if 'grupo' in f][0]

grupo = importlib.import_module(module_file)

successfulSamples = [
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
        {'customers': ['first_name', 'last_name']}
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
        {'customers': ['edad', 'first_name', 'last_name', 'pais']}
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
        {'customers': ['edad', 'first_name', 'id', 'last_name']}
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
    # Testing SELECT, FROM, LEFT JOIN, GROUP BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        LEFT JOIN phones_numbers AS p ON customers.id = p.customer_id 
        GROUP BY customers.first_name, customers.last_name
        ''',
        {'customers': ['first_name', 'id', 'last_name'],
         'phones_numbers': ['customer_id']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, LEFT JOIN, GROUP BY, ORDER BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        LEFT JOIN phones_numbers AS p ON customers.id = p.customer_id 
        GROUP BY customers.first_name, customers.last_name
        ORDER BY customers.edad ASC, customers.pais
        ''',
        {'customers': ['edad', 'first_name', 'id', 'last_name', 'pais'],
         'phones_numbers': ['customer_id']}
    ),

    ##############################################################################
    # Testing SELECT, FROM, LEFT JOIN, GROUP BY, HAVING, ORDER BY
    ##############################################################################
    (
        # Should be ok
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        LEFT JOIN phones_numbers AS p ON customers.id = p.customer_id 
        GROUP BY customers.first_name, customers.last_name
        HAVING customers.edad > 18
        ORDER BY customers.edad ASC, customers.pais
        ''',
        {'customers': ['edad', 'first_name', 'id', 'last_name', 'pais'],
         'phones_numbers': ['customer_id']}
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
    # Testing SELECT, DISTINCT, FROM, LEFT JOIN - ON, WHERE, GROUP BY, HAVING
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
        HAVING customers.edad > 18
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
    # Testing SELECT, DISTINCT, FROM - AS, LEFT JOIN - ON, WHERE, GROUP BY, HAVING, ORDER BY
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
        HAVING customers.edad > 18
        ORDER BY c.edad ASC, c.pais
        ''',
        {'customers': ['edad', 'id', 'pais', 'phone'],
         'phones_numbers': ['customer_id', 'phone', 'prefijo']}
    ),
]


##############################################################################
##################################  ERRORS  ##################################
##############################################################################

unsuccessfulSamples = [
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
        {'message': 'El alias de la tabla debe coincidir con lo antepuesto en el campo. Revea su consulta'}
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
        {'message': 'El alias de la tabla debe coincidir con lo antepuesto en el campo. Revea su consulta'}
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
        {'message': 'El alias de la tabla debe coincidir con lo antepuesto en el campo. Revea su consulta'}
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
        {'message': 'El alias de la tabla debe coincidir con lo antepuesto en el campo. Revea su consulta'}
    ),

    ##############################################################################
    # Testing SELECT, FROM, LEFT JOIN, GROUP BY, HAVING, ORDER BY
    # This has an undefined alias in consult 'ON'
    ##############################################################################
    (
        # Should throw error
        '''
        SELECT customers.first_name, customers.last_name
        FROM customers
        LEFT JOIN phones_numbers AS p ON c.id = p.customer_id 
        GROUP BY customers.first_name, customers.last_name
        HAVING customers.edad > 18
        ORDER BY customers.edad ASC, customers.pais
        ''',
        {'message': 'El alias de la tabla debe coincidir con lo antepuesto en el campo. Revea su consulta'}
    ),
]


##################################################################################################
##################################  Testing Successful samples  ##################################
##################################################################################################
counterSuccSamples = 0
totalSuccSamples = len(successfulSamples)
print(Fore.GREEN + '/' * 30, ' SUCCESSFUL QUERYES', '/' * 30)
print(Fore.WHITE)
for ix, sample in enumerate(successfulSamples):
    print(Fore.LIGHTYELLOW_EX +
          '*************** Resultados test parsing ejemplo {} ***************'.format(ix+1) + Fore.WHITE)
    print(sample[0])
    print('-' * 3, ' Fin consulta ', '-' * 3)

    try:
        result = grupo.parse_select_statement(sample[0])

        if result != sample[1]:
            resultStr = 'incorrecto'
            print(Fore.RED)

        else:
            resultStr = 'correcto'
            print(Fore.GREEN)
            counterSuccSamples += 1

        print('El resultado de la comprobación fue {} !'.format(resultStr))
        print(Fore.WHITE + 'Resultado entregado: ', result)
        print('Resultado esperado: ', sample[1])

    except Exception as e:
        print('''Se produjo una excepción al intentar parsear el ejemplo y/o 
                 comprobar el resultado !''')
        print(e)
    print(Fore.LIGHTYELLOW_EX +
          '*************** FIN test parsing ejemplo        {} ***************'.format(ix+1) + Fore.WHITE)
    print('')
    print('')

##################################################################################################
##################################  Testing Unsuccessful samples  ################################
##################################################################################################
counterUnsuccSamples = 0
totalUnsuccSamples = len(unsuccessfulSamples)
print(Fore.GREEN + '/' * 30, ' UNSUCCESSFUL QUERYES', '/' * 30)
print(Fore.WHITE)
for ix, sample in enumerate(unsuccessfulSamples):
    print(Fore.LIGHTYELLOW_EX +
          '*************** Resultados test parsing ejemplo {} ***************'.format(ix+1) + Fore.WHITE)
    print(sample[0])
    print('-' * 3, ' Fin consulta ', '-' * 3)

    try:
        result = grupo.parse_select_statement(sample[0])

        if result.strerror != sample[1]:
            resultStr = 'incorrecto'
            print(Fore.RED)

        else:
            resultStr = 'correcto'
            counterUnsuccSamples += 1
            print(Fore.GREEN)

        print('El resultado de la comprobación fue {} !'.format(resultStr))
        print(Fore.WHITE + 'Resultado entregado: ', result)
        print('Resultado esperado: ', sample[1])

    except Exception as e:
        print('''Se produjo una excepción al intentar parsear el ejemplo y/o 
                 comprobar el resultado !''')
        print(e)
    print(Fore.LIGHTYELLOW_EX +
          '*************** FIN test parsing ejemplo        {} ***************'.format(ix+1) + Fore.WHITE)
    print('')
    print('')

print(Fore.GREEN + '/' * 30, ' Passed successful samples ', '= ',
      counterSuccSamples, ' / ', totalSuccSamples, '/' * 30)
print('/' * 30, ' Passed unsuccessful samples ', '= ',
      counterUnsuccSamples, ' / ', totalUnsuccSamples, '/' * 30)
