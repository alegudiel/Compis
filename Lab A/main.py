"""
Ale Gudiel 19232

--------Laboratorio A--------

Este laboratorio consiste en la implementación de un subconjunto de algoritmos básicos de
autómatas finitos y expresiones regulares. Deberá desarrollar un programa que acepte como
entrada una expresión regular 𝑟 .
A partir de 𝑟 deberá construir un AFN (NFA)

Especificación del funcionamiento del programa
● Entrada
    o Una expresión regular 𝑟 .
● Salida
    o Por cada AFN (NFA) generado a partir de 𝑟 :
        ▪ una imagen con el Grafo correspondiente para el AF generado, mostrando el estado inicial, los estados adicionales, el estado de
"""

# Importamos las librerías necesarias.
from evaluateRegex import infixToPostfix
# from afnBuild import *

# Pedimos la expresión regular (regex) al usuario.
r = input("Ingrese la expresión regular: ")

# Convertimos a postfix
postfixVal = infixToPostfix(r)
print("La expresión regular en notación postfix es: ", postfixVal)

# Convertimos de postfix a NFA
# nfaValue = postfixToAFN(postfixVal)
    # Mostramos el NFA
# printAutomaton(str(nfaValue))

# Mostramos el grafo del NFA

# Mostramos el grafo del NFA reducido

