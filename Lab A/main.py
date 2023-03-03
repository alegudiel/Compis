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
###### ----> Ejemplos del pre-lab
# print(infixToPostfix('ab ∗ ab ∗'))
# print(infixToPostfix('0? (1? )? 0 ∗')) 
# print(infixToPostfix('(a*|b*)c')) 
# print(infixToPostfix('(b|b)*abb(a|b)*')) 
# print(infixToPostfix('(a|ε)b(a+)c?'))
# print(infixToPostfix('(a|b)*a(a|b)(a|b)'))


# Importamos las librerías necesarias.
from validations import checkForErrors
from toPostfix import showPostfix
from buildAFN import thompsonConstruction
from showThings import printNFA, nfaGraph

# Pedimos la expresión regular (regex) al usuario.
r = input("\nIngrese la expresión regular: ")
print('-----------------------------------------')

# Pasamos el regex a postfix
# Aqui mismo se valida y formatea
showPostfix(r)

# Convertimos de postfix a NFA
#     print('--->Convertimos de postfix a NFA...')
#     nfaValue = thompsonConstruction(cleanedExp)
        
#         # Mostramos el NFA
#     print('---------------------------------------------------')
#     printNFA(nfaValue)
        
#         # Mostramos el grafo del NFA
#     print('---------------------------------------------------')
#     print("--->Convertimos el NFA a un grafo...")
#     print('---------------------------------------------------')
#     nfaGraph(nfaValue)


# else: print("Los errores encontrados son ---> ", checkedExp)


