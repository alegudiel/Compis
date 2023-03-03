"""
Funcion que convierte una expresión regular en notación infija a una expresión regular en notación posfija.
"""
from validations import checkForErrors

def addImplicitConcatenation(r):
    # Add implicit concatenation
    new_r = ""
    for i in range(len(r)):
        c = r[i]
        new_r += c
        if c == '(' or c == '|':
            continue
        if i < len(r)-1:
            next_c = r[i+1]
            if next_c == '*' or next_c == ')' or next_c == '|':
                continue
            if next_c.isalnum() or next_c == 'ε':
                new_r += '.'
    return new_r

def isBalanced(r):
    stack = []
    for c in r:
        if c == '(':
            stack.append(c)
        elif c == ')':
            if not stack:
                return False
            stack.pop()
    return not stack

def infixToPostfix(infix):
    # Eliminar espacios y agregar concatenación implícita
    infix = infix.replace(' ', '') 
    infix = infix.replace('?', 'ε')
    infix = addImplicitConcatenation(infix)

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
            output.append(output.pop() + '*')
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

def showPostfix(r):
    # Verificar que la expresión regular no tenga errores
    errors = checkForErrors(r)

    if errors:
        print('La expresión regular tiene errores: \n')
        for e in errors:
            print(e)
        return
    
    else:
        print('\nLa expresión regular no tiene errores')

        # Verificar que la expresión regular esté balanceada
        if not isBalanced(r):
            print('\nLa expresión regular no está balanceada')
            return
        
        print("-----------------------------------------")
        print("\nLa expresión esta balanceada y es válida") 
        print("Expresión balanceada: ", addImplicitConcatenation(r))
        print("-----------------------------------------")
        # Convertir la expresión regular a notación posfija
        postfix = infixToPostfix(r)

        # Imprimir la expresión regular en notación posfija
        print('\nNotación posfija:', postfix)
        print("-----------------------------------------")