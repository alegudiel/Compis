"""
Funciones de validación de datos del regex ingresado por el usuario
"""

def hasUnbalanced(r, open_char, close_char):
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
    return r[0] in ('*', '|', '?', '+', '.')

def checkForErrors(r):
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