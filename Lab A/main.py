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
# print(infixToPostfix('ab ∗ ab ∗')) ### ---> postfix ab.*ab.*
# print(infixToPostfix('0? (1? )? 0 ∗')) ### ---> postfix 0?1?  ?0  ∗
# print(infixToPostfix('(a*|b*)c')) ### ---> postfix a*b*|c
# print(infixToPostfix('(b|b)*abb(a|b)*')) ### ---> postfix bb|abbab|**
# print(infixToPostfix('(a|ε)b(a+)c?')) ### ---> postfix a|εba+c?
# print(infixToPostfix('(a|b)*a(a|b)(a|b)')) ### ---> postfix ab|aab|ab|*


# Importamos las librerías necesarias.
from validations import checkForErrors
from formating import cleanRegex
from toPostfix import infixToPostfix
from buildAFN import thompsonConstruction, printNFA
from showAFNGraph import nfaGraph

# Pedimos la expresión regular (regex) al usuario.
print('---------------------------------------------------')
r = input("Ingrese la expresión regular: ")
print('---------------------------------------------------')
print("La expresión regular ingresada es:", r)

# Revisamos que la expresión regular sea válida.
checkedExp = checkForErrors(r)
if checkForErrors(r) == []:
    # Si no hay errores, procedemos a formatear la expresión regular.
    cleanedExp = cleanRegex(r)

    print("--->Se validó la expresión...")
    print('---------------------------------------------------')
    print("--->La expresión regular se está formateando...")
    print('---------------------------------------------------')
    print("La expresión regular formateada es:", cleanedExp)
    print('---------------------------------------------------')

    # Convertimos a postfix en caso de que no haya errores.
    print("--->Convertimos a postfix...")
    print('---------------------------------------------------')
    ########### para descomentar una vez que se implemente la función cleanRegex
    postfixValue = infixToPostfix(cleanedExp)
    # postfixValue = infixToPostfix(r)
    print("La expresión regular en postfix es:", postfixValue)
    print('---------------------------------------------------')

    # Convertimos de postfix a NFA
    print('--->Convertimos de postfix a NFA...')
    nfaValue = thompsonConstruction(postfixValue)
    
    # Mostramos el NFA
    print('---------------------------------------------------')
    printNFA(nfaValue)
    
    # Mostramos el grafo del NFA
    print('---------------------------------------------------')
    print("--->Convertimos el NFA a un grafo...")
    print('---------------------------------------------------')
    nfaGraph(nfaValue)


else:
    print("Los errores encontrados son ---> ", checkedExp)



