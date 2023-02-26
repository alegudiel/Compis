# A partir de una expresion regular r, 
# convertimos a notacion infix,
# luego a notacion postfix usando el algoritmo Shunting Yard.
import re
from collections import deque
from formating import cleanRegex

#### Funcion que determina si un caracter es un operador.
# def infixToPostfix(r):
#     # Precendencia de operadores
#     prec = {
#         '(': 1,
#         '|': 2,
#         '.': 3,
#         '?': 4,
#         '*': 4,
#         '∗': 4,
#         '+': 4,
#         '^': 5,
#         'ε': 6,
#     }

#     # Agregar entradas para cada letra
#     for letter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
#         prec[letter] = 7

#     # Convertir la expresión regular a una lista de tokens
#     #tokens = re.findall(r'[()∗|.+?ɛ]|(?:\\.|[^\w()?+∗|])+|[\wɛ]+', r)
#     tokens = re.findall(r'[()∗|.?+ɛ]|(?:\\.|[^\w()?+∗|])+|[\wɛ]', r)

#     # Deque para almacenar la salida y la pila de operadores
#     output = deque()
#     operatorStack = deque()

#     # Algoritmo Shunting Yard
#     for token in tokens:
#         if re.match(r'[\wɛ]+', token):
#             prec_token = prec[token]
#             output.append(token)
#         elif token == '∗':
#             output.append('.')
#             output.append(token.replace('∗', '*'))
#         elif token == 'ɛ':
#             output.append(token)
#         elif token == '(':
#             operatorStack.append(token)
#         elif token == ')':
#             while operatorStack[-1] != '(':
#                 output.append(operatorStack.pop())
#             operatorStack.pop()
#         elif token == '[':
#             operatorStack.append(token)
#             output.append(token)
#         elif token == ']':
#             while operatorStack[-1] != '[':
#                 output.append(operatorStack.pop())
#             output.append(operatorStack.pop())
#         elif token == '{':
#             operatorStack.append(token)
#             output.append(token)
#         elif token == '}':
#             while operatorStack[-1] != '{':
#                 output.append(operatorStack.pop())
#             output.append(operatorStack.pop())
#         elif token == ' ':
#             continue
#         else:
#             while operatorStack and prec[operatorStack[-1]] >= prec[token]:
#                 output.append(operatorStack.pop())
#             operatorStack.append(token)

#     while operatorStack:
#         output.append(operatorStack.pop())

#     if len(output) > 1 and output[-2] not in {'('} and output[-1] not in {')', '|'}:
#         output += '.'
#     if output[-1] != ')' and len(operatorStack) != 0:
#         output.append('.')


#     # Convertir la salida de la cola doble a una cadena
#     return ''.join(output)

def infixToPostfix(r):
    # Precendencia de operadores
    prec = {
        '(': 1,
        '|': 2,
        '.': 3,
        '?': 4,
        '*': 4,
        '+': 4,
        '^': 5,
        'ε': 6,
    }

    # Agregar entradas para cada letra
    for letter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
        prec[letter] = 7

    # Formatear la expresión regular
    r = cleanRegex(r)

    # Convertir la expresión regular a una lista de tokens
    tokens = list(r)

    # Lista para almacenar la salida y la pila de operadores
    output = []
    operatorStack = []

    # Algoritmo Shunting Yard
    for token in tokens:
        if token in prec:
            while operatorStack and prec[operatorStack[-1]] >= prec[token]:
                output.append(operatorStack.pop())
            operatorStack.append(token)
        else:
            output.append(token)

    while operatorStack:
        output.append(operatorStack.pop())

    # Convertir la salida de la lista a una cadena
    return ''.join(output)
