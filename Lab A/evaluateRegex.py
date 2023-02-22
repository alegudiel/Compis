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
        '?': 5,
        '^': 6,
        'ε': 7,
    }

    # Agregar entradas para cada letra
    for letter in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
        prec[letter] = 8

    # Convertir la expresión regular a una lista de tokens
    #tokens = re.findall(r'[()∗*|.+?ɛ]|(?:\\.|[^\w()?+*∗|])+|[\wɛ]+', r)
    tokens = re.findall(r'[()∗*|.?+ɛ]|(?:\\.|[^\w()?+*∗|])+|[\wɛ]', r)

    # Deque para almacenar la salida y la pila de operadores
    output = deque()
    operatorStack = deque()

    # Algoritmo Shunting Yard
    for token in tokens:
        if re.match(r'[\wɛ]+', token):
        #     output.append(token)
        # elif re.match(r'[\wɛ]+', token): 
        # --> para poder verificar que se revise cada letra
            prec_token = prec[token]
            output.append(token)
        # --> para poder tomar en cuenta  ∗
        elif token == '∗':
            output.append('.')
            output.append(token.replace('∗', '*'))
        elif token == 'ɛ':
            output.append(token)
        elif token == '(':
            operatorStack.append(token)
        elif token == ')':
            while operatorStack[-1] != '(':
                output.append(operatorStack.pop())
            operatorStack.pop()
        # --> para poder tomar en cuenta los espacios en blanco
        elif token == ' ':
            continue
        else:
            while operatorStack and prec[operatorStack[-1]] >= prec[token]:
                output.append(operatorStack.pop())
            operatorStack.append(token)

    while operatorStack:
        output.append(operatorStack.pop())

    # Convertir la salida de la cola doble a una cadena
    return ''.join(output)


###### ----> Ejemplos del pre-lab
print(infixToPostfix('ab ∗ ab ∗'))
print(infixToPostfix('0? (1? )? 0 ∗'))
print(infixToPostfix('(a*|b*)c'))
print(infixToPostfix('(b|b)*abb(a|b)*'))
print(infixToPostfix('(a|ε)b(a+)c?'))
print(infixToPostfix('(a|b)*a(a|b)(a|b)'))