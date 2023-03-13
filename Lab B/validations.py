"""
Funciones de validación de datos del regex ingresado por el usuario
"""

def addImplicitConcatenation(r):
    """
    Agrega concatenación implícita a la expresión regular.
    """
    new_expression = ""
    for i in range(len(r)):
        c = r[i]
        new_expression += c
        if c == '(' or c == '|':
            continue
        if i < len(r)-1:
            next_c = r[i+1]
            if next_c == '*' or next_c == ')' or next_c == '|':
                continue
            if next_c.isalnum() or next_c == 'ε':
                new_expression += '.'
    return new_expression

def hasUnbalanced(r, open_char, close_char):
    """
    Verifica si la expresión regular está balanceada.
    """
    stack = []
    for c in r:
        if c == open_char:
            stack.append(c)
        elif c == close_char:
            if not stack:
                return True
            stack.pop()
    return bool(stack)

def hasOperatorAtStart(r):
    """
    Verifica si la expresión regular tiene operadores al inicio.
    """
    return r[0] in ('*', '|', '?', '+', '.')

def checkForErrors(r):
    """
    Verifica si la expresión regular tiene errores.
    """
    errors = []
    if hasUnbalanced(r, '(', ')'):
        errors.append('La expresión regular tiene paréntesis desbalanceados.')
    if hasUnbalanced(r, '[', ']'):
        errors.append('La expresión regular tiene corchetes desbalanceados.')
    if hasUnbalanced(r, '{', '}'):
        errors.append('La expresión regular tiene llaves desbalanceadas.')
    if hasOperatorAtStart(r):
        errors.append('La expresión regular tiene operadores al inicio.')

    return errors