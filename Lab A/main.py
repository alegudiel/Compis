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
from evaluateRegex import infixToPostfix
from buildAFN import thompsonConstruction, printNFA
from showAFNGraph import nfaGraph

# Pedimos la expresión regular (regex) al usuario.
r = input("Ingrese la expresión regular: ")

# Revisamos que la expresión regular sea válida.
checkedExp = checkForErrors(r)
if checkForErrors(r) == []:
    # Convertimos a postfix en caso de que no haya errores.
    postfixValue = infixToPostfix(r)
    print("La expresión regular en postfix es: ", postfixValue)
    # Convertimos de postfix a NFA
    nfaValue = thompsonConstruction(postfixValue)
    
    # Mostramos el NFA
    printNFA(nfaValue)
    
    # Mostramos el grafo del NFA
    nfaGraph(nfaValue)

    


    
        


else:
    print("Los errores encontrados son ---> ", checkedExp)



# Mostramos el grafo del NFA reducido

