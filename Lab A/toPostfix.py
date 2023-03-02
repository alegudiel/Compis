from collections import deque

def infixToPostfix(r):
    # Precendencia de operadores
    PRECEDENCE = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}

    # Convertir la expresión regular a una lista de tokens
    tokens = []
    i = 0
    while i < len(r):
        c = r[i]
        if c.isalnum() or c == 'ε':
            tokens.append(c)
            if i < len(r) - 1 and r[i+1] not in '|.?+*()ɛ∗[]{}':
                tokens.append('.')
        elif c in '|.?+*()ɛ∗[]{}':
            tokens.append(c)
        elif c == '\\':
            tokens.append(r[i:i+2])
            i += 1
            if i < len(r) - 1 and r[i+1] not in '|.?+*()ɛ∗[]{}':
                tokens.append('.')
        i += 1

    # Deque para almacenar la salida y la pila de operadores
    output = deque()
    operatorStack = deque()

    # Algoritmo Shunting Yard
    for token in tokens:
        if token.isalnum():
            if token == 'ε':
                output.append('')
            else:
                output.append(token)
        elif token == '∗':
            output.append(token.replace('∗', '*'))
        elif token == '(':
            operatorStack.append(token)
        elif token == ')':
            while operatorStack[-1] != '(':
                output.append(operatorStack.pop())
            operatorStack.pop()
        elif token == '[':
            operatorStack.append(token)
            output.append(token)
        elif token == ']':
            while operatorStack[-1] != '[':
                output.append(operatorStack.pop())
            output.append(operatorStack.pop())
        elif token == '{':
            operatorStack.append(token)
            output.append(token)
        elif token == '}':
            while operatorStack[-1] != '{':
                output.append(operatorStack.pop())
            output.append(operatorStack.pop())
        else:
            while operatorStack and PRECEDENCE.get(operatorStack[-1], 0) >= PRECEDENCE.get(token, 0):
                output.append(operatorStack.pop())
            operatorStack.append(token)

    while operatorStack:
        output.append(operatorStack.pop())

    # Convertir la salida de la cola doble a una cadena
    return ''.join(output)
