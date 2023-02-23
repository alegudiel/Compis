import re

# Función que determina si un caracter es un operador.
def hasOperators(r):
    return bool(re.findall(r'[()∗*|.?+ɛ\[\]{}]', r))

# Función que determina si la expresión regular tiene paréntesis desbalanceados.
def hasUnbalancedParentheses(r):
    stack = []
    for c in r:
        if c == '(':
            stack.append(c)
        elif c == ')':
            if not stack:
                return True
            stack.pop()
    return bool(stack)

# Función que determina si la expresión regular tiene corchetes desbalanceados.
def hasUnbalancedBrackets(r):
    stack = []
    for c in r:
        if c == '[':
            stack.append(c)
        elif c == ']':
            if not stack:
                return True
            stack.pop()
    return bool(stack)

# Función que determina si la expresión regular tiene llaves desbalanceadas.
def hasUnbalancedBraces(r):
    stack = []
    for c in r:
        if c == '{':
            stack.append(c)
        elif c == '}':
            if not stack:
                return True
            stack.pop()
    return bool(stack)

# Función que determina si la expresión regular tiene secuencias de escape inválidas.
def hasInvalidEscape(r):
    try:
        eval(f'"{r}"')
    except:
        return True
    return False

# Función que determina si la expresión regular tiene caracteres no válidos.
def hasValidCharacters(r):
    return bool(re.match(r'[()∗*|.?+ɛ]|(?:\\.|[^\w()?+*∗|])+|[\wɛ]', r))

def checkForErrors(r):
    errors = []
    if not hasOperators(r):
        errors.append('La expresión regular no tiene operadores válidos.')
    if hasUnbalancedParentheses(r):
        errors.append('La expresión regular tiene paréntesis desbalanceados.')
    if hasUnbalancedBrackets(r):
        errors.append('La expresión regular tiene corchetes desbalanceados.')
    if hasUnbalancedBraces(r):
        errors.append('La expresión regular tiene llaves desbalanceadas.')
    if hasInvalidEscape(r):
        errors.append('La expresión regular tiene secuencias de escape inválidas.')
    if not hasValidCharacters(r):
        errors.append('La expresión regular tiene caracteres no válidos.')
    return errors
    # En caso de que la expresión regular no tenga errores, se retorna una lista vacía.

