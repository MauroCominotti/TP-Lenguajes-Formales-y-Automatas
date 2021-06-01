# TP Lenguajes Formales y Autómatas
## Integrantes
- Carena Pablo
- Cominotti Mauro
- Yacovino Juan
## Enlace al repositorio
> https://github.com/MauroCominotti/TP-Lenguajes-Formales-y-Automatas

## 1)	Enunciado

Se debe escribir un programa que genere un parser capaz de analizar una sentencia SQL de tipo SELECT y extraer de la misma los siguientes elementos:
-	Listado de tablas utilizadas
-	Columnas utilizadas por cada una de las tablas, independientemente de la cláusula en la que se la utilice

Las particularidades que debe contemplar la consulta de entrada se describen a continuación:
Consulta: SELECT
Cláusulas opcionales a ser contempladas:
-	FROM (puede contener uno o más INNER JOIN y/o LEFT JOIN, y la opción AS como alias para las tablas)
-	WHERE (puede contener consultas anidadas IN)
-	GROUP BY
-	HAVING
-	ORDER BY

Funciones a ser contempladas (en las cláusulas que permiten utilizarlas):
-	MIN
-	MAX
-	COUNT (podría utilizarse el operador DISTINCT)

Restricciones:
-	No se deberá contemplar la utilización de * como abreviación de todas las columnas existentes.

## 2)	Consignas

a.	Utilizando la herramienta PLY, escriba el código necesario correspondiente a los módulos lex (tokens) y yacc (reglas) que codifiquen una gramática capaz de reconocer la sentencia requerida en el enunciado. (60 puntos)

b.	Incorporar al código desarrollado en el punto previo la lógica necesaria para obtener las tablas y columnas utilizadas en la consulta. (30 puntos)

c.	Desarrolle una función denominada parse_select_statement que reciba como parámetro una consulta SELECT y devuelva como resultado un diccionario. Dicho diccionario tendrá como claves los nombres de las tablas y como valor el listado de columnas ordenado alfabéticamente. (10 puntos)

## Generalidades

-	El trabajo se aprueba con 80 puntos.
-	Fecha límite de entrega: 11/06/2021 23:59
-	Coloquio: 15/06/2021
-	Todo el código desarrollado debe incluirse en un archivo denominado grupoxx.py donde xx es el número de grupo correspondiente.
-	El código entregado no debe imprimir ningún valor en pantalla (excluir sentencias print).
-	Forma de entrega: correo electrónico (marianoferrero.mf@gmail.com y arielrossanigo@gmail.com) incluyendo un enlace a un repositorio de código público (GitHub, BitBucket o GitLab) 
-	Se debe utilizar Python 3
-	Número máximo de integrantes por grupo: 3
-	Número mínimo de integrantes por grupo: 2
-	Los integrantes de cada grupo se deben comunicar antes del 23/04/2021 en el foro de la materia. El orden en el que se envíe esa comunicación definirá el número de grupo (ejemplo: el primero en enviar será automáticamente el grupo 1, y así sucesivamente).

### Anotaciones
> USAR TRANSACT SQL, Usar solo tipos de datos "strings" y "numeros", y por más que se genere una tabla usamos siempre el alias (una vez que tenemos los alias una vez que reconocemos las columnas decimos tal columna es de tal tabla); el AS puede ir como no; el DISTINCT en el SELECT NO VA; el JOIN va solo INNER o LEFT; al usar desigualdad usamos tenemos que ver si usamos el "!=", no usamos el "IS NOT"; en el SELECT pueden NO estar columnas que se toman en el GROUP BY, eso es el análisis semántico, se ocupará otro analizador; palabras reservadas siempre con MAYUSCULAS


### GRAMÁTICA
Terminales: Mayuscula
No terminales: Minuscula

```SQL
query : SELECT columnas FROM tablas
      | SELECT columnas FROM tablas joins WHERE condiciones
      | SELECT columnas FROM tablas joins WHERE condiciones GROUP BY columnas_group_by
      | SELECT columnas FROM tablas joins WHERE condiciones GROUP BY columnas_group_by HAVING condicion_having
      | SELECT columnas FROM tablas joins WHERE condiciones GROUP BY columnas_group_by HAVING condicion_having ORDER BY columnas_order_by

columnas : columna 
         | columna COMA columnas
columna : ID PUNTO ID 
        | ID PUNTO ID AS COMILLA ID COMILLA
        | func_resumen AS COMILLA ID COMILLA
columnas_group_by : ID PUNTO ID
                  | ID PUNTO ID COMA columnas_group_by
columnas_order_by : ID PUNTO ID orden
                  | ID PUNTO ID orden COMMA columnas_order_by

orden : ASC
      | DESC
condicion_having : func_resumen signo valor

func_resumen : MIN PAREN_IZQ ID PUNTO ID PAREN_DER
             | MAX PAREN_IZQ ID PUNTO ID PAREN_DER
             | COUNT PAREN_IZQ ID PUNTO ID PAREN_DER
             | COUNT PAREN_IZQ DISTINCT ID PUNTO ID PAREN_DER

tablas : tabla 
       | tabla COMA tabla
       
tabla : ID AS ID 
      | ID ID

joins : INNER JOIN tabla ON condiciones

condiciones : condicion
            | ID PUNTO ID subconsulta
            | condiciones AND condiciones
            | condiciones OR condiciones
            | PAREN_IZQ condiciones OR condiciones PAREN_DER

subconsulta : IN PAREN_IZQ query PAREN_DER
            | NOT IN PAREN_IZQ query PAREN_DER

condicion : ID PUNTO ID SIGNO VALOR
          | ID PUNTO ID SIGNO ID PUNTO ID
          | ID PUNTO ID nulleable
          | ID PUNTO ID IGUAL booleano

signo : MENOR_IZQ | MAYOR_IZQ | MEN_IGUAL_IZQ | MAY_IGUAL_IZQ | IGUAL | DESIGUAL
valor : ID
      | NUMERO
nulleable : NULL
          | IS NOT NULL
booleano : TRUE
         | FALSE


### EJEMPLOS PARA PROBAR
python grupo02.py

SELECT P.nombre, P.apellido FROM Personas P INNER JOIN Empleados E ON E.Dni = P.Dni WHERE condiciones GROUP BY P.nombre, P.apellido, P.dni, P.Sectores HAVING COUNT(P.sectores) ORDER BY P.nombre DESC

```