import re
from collections import deque

# Función que determina si un caracter es un operador.
def hasOperators(r):
    return bool(re.findall(r'[()∗*|.?+ɛ\[\]{}]', r))

# Función que determina si la expresión regular tiene paréntesis, corchetes o llaves desbalanceados.
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

# Función que determina si la expresión regular tiene caracteres no válidos.
def hasValidCharacters(r):
    return bool(re.match(r'[()∗*|.?+ɛ]|(?:\\.|[^\w()?+*∗|])+|[\wɛ]', r))

# Función que determina si un operador esta al inicio, no pueda ser el primer caracter.
def hasOperatorAtStart(r):
    return bool(re.match(r'^[∗*|.?+ɛ]', r))

# Función que determina si una expresión tiene operadores dobles 
# (ej: **, ++, ||, etc.)
def hasDoubleOperators(r):
    return bool(re.match(r'[∗*|.?+ɛ]{2,}', r))

# Función que determina si le falta otro caracter para completar la expresión regular.
def hasMissingCharacter(r):
    return bool(re.match(r'[∗*|.?+ɛ]{1}', r))

# Función que determina si no hay un operador entre dos caracteres.
def hasMissingOperator(r):
    return bool(re.match(r'[∗*|.?+ɛ]{1}', r))

# Función que verifica si la expresión regular tiene errores de sintaxis.
def checkForErrors(r):
    errors = []
    if not hasOperators(r):
        errors.append('La expresión regular no tiene operadores válidos. Prueba con: (, ), *, |, ?, +, ., ε, [, ], {, }')
    if hasUnbalanced(r, '(', ')'):
        errors.append('La expresión regular tiene paréntesis desbalanceados.')
    if hasUnbalanced(r, '[', ']'):
        errors.append('La expresión regular tiene corchetes desbalanceados.')
    if hasUnbalanced(r, '{', '}'):
        errors.append('La expresión regular tiene llaves desbalanceadas.')
    if not hasValidCharacters(r):
        errors.append('La expresión regular tiene caracteres no válidos. Incluye caracteres especiales como: $, #, @, etc.')
    if hasOperatorAtStart(r):
        errors.append('La expresión regular tiene operadores al inicio.')
    if hasDoubleOperators(r):
        errors.append('La expresión regular tiene operadores seguidos que no pueden operarse.')
    # En caso de que la expresión regular no tenga errores, se retorna una lista vacía.
    return errors