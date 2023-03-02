# This file contains the functions that validate the regular expression    
def isBalanced(self):
    stack = []
    for char in self.regex:
        if char == '(' or char == '[' or char == '{' :
            stack.append(char)
        elif char == ')' or char == ']' or char == '}':
            if not stack:
                return False
            stack.pop()
    return not stack

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