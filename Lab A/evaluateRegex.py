# A partir de una expresion regular r, 
# convertimos a notacion infix,
# luego a notacion postfix usando el algoritmo Shunting Yard.
import re
from collections import deque

# Funcion que determina si un caracter es un operador.
def infixToPostfix(r):
    # Precendencia de operadores
    prec = {
        '(': 1,
        '|': 2,
        '.': 3,
        '?': 4,
        '*': 4,
        '∗': 4,
        '+': 4,
        '^': 5,
        'ɛ': 6,
        '\w': 7,
    }

    # Convertir la expresión regular a una lista de tokens
    tokens = re.findall(r'[()∗*|.?+ɛ]|(?:\\.|[^\w()?+*∗|])+|[\wɛ]+', r)

    # Deque para almacenar la salida y la pila de operadores
    output = deque()
    op_stack = deque()

    # Algoritmo Shunting Yard
    for token in tokens:
        if re.match(r'[\wɛ]+', token):
            output.append(token)
        elif token == 'ɛ':
            output.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack[-1] != '(':
                output.append(op_stack.pop())
            op_stack.pop()
        else:
            while op_stack and prec[op_stack[-1]] >= prec[token]:
                output.append(op_stack.pop())
            op_stack.append(token)

    while op_stack:
        output.append(op_stack.pop())

    # Convertir la salida de la cola doble a una cadena
    return ''.join(output)


###### ----> Ejemplos del pre-lab
# print(infixToPostfix('ab∗ab∗'))
# print(infixToPostfix('0?(1?)?0∗'))
# print(infixToPostfix('(a*|b*)c'))
# print(infixToPostfix('(b|b)*abb(a|b)*'))
# print(infixToPostfix('(a|ε)b(a+)c?'))
# print(infixToPostfix('(a|b)*a(a|b)(a|b)'))