"""
Funcion que convierte una expresión regular en notación infija a una expresión regular en notación posfija.
"""
from validations import addImplicitConcatenation

def infixToPostfix(infix):
    infix = infix.replace(' ', '')  # Eliminar espacios
    infix = infix.replace('?', '|ε') # Reemplazar ? por |ε
    infix = addImplicitConcatenation(infix) # Agregar concatenación implícita

    # Diccionario de precedencia de operadores
    precedence = {'(': 1, '|': 2, '.': 3, '?': 4, '*': 4, '+': 4}

    # Pila de operadores y lista de salida
    operatorStack = []
    output = []

    # Leer la expresión infix de izquierda a derecha
    i = 0
    while i < len(infix):
        c = infix[i]
        if c.isalnum() or c == 'ε':
            # Operando
            output.append(c)
        elif c == '+':
            # Operador unario
            while operatorStack and precedence.get(operatorStack[-1], 0) >= precedence.get(c, 0):
                output.append(operatorStack.pop())
            output.append(output.pop())
            operatorStack.append(c)
        elif c == '(':
            # Paréntesis izquierdo
            operatorStack.append(c)
        elif c == ')':
            # Paréntesis derecho
            while operatorStack[-1] != '(':
                output.append(operatorStack.pop())
            operatorStack.pop()
        else:
            # Operador
            while operatorStack and precedence.get(operatorStack[-1], 0) >= precedence.get(c, 0):
                output.append(operatorStack.pop())
            operatorStack.append(c)
        i += 1

    # Sacar los operadores restantes de la pila y agregarlos a la lista de salida
    while operatorStack:
        output.append(operatorStack.pop())

    # Unir la lista de salida en una sola cadena y retornar
    return ''.join(output)

