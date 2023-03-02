def hasOperators(r):
    operators = set('()*|?.+[]{}')
    return any(c in operators for c in r)

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

def hasValidCharacters(r):
    for c in r:
        if not c.isalnum() and c not in ('()', '.*', '|', '?', '+', '[', ']', '{', '}', '\\'):
            return False
    return True

def hasOperatorAtStart(r):
    return r[0] in ('*', '|', '?', '+', '.')

def hasDoubleOperators(r):
    for i in range(len(r) - 1):
        if r[i] in ('*', '|', '?', '+', '.') and r[i + 1] in ('*', '|', '?', '+', '.'):
            return True
    return False

def hasMissingCharacter(r):
    return r[-1] in ('*', '|', '?', '+', '.', '[') or r.endswith('\\')

def hasMissingOperator(r):
    for i in range(len(r) - 1):
        if r[i].isalnum() and r[i + 1].isalnum():
            return True
    return False

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
    # if hasDoubleOperators(r):
    #     errors.append('La expresión regular tiene operadores seguidos que no pueden operarse.')
    if hasMissingCharacter(r):
        errors.append('La expresión regular está incompleta. Falta otro caracter.')
    # if hasMissingOperator(r):
    #     errors.append('La expresión regular tiene dos caracteres consecutivos sin operador.')
    return errors
