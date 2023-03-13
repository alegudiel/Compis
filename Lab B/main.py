"""
Ale Gudiel 19232

--------Laboratorio B--------

Este laboratorio consiste en la implementación de un subconjunto de algoritmos básicos de autómatas finitos y expresiones regulares. Deberá desarrollar un programa que acepte como entrada una expresión regular 𝑟 y una cadena 𝑤 .
Este laboratorio combina el trabajo generado en el Laboratorio A y lo extiende para desarrollar la base del generador de analizadores léxicos.
A partir de 𝑟 deberá construir un AFN (NFA), el cual deberá transformar posteriormente a un AFD (DFA); además, deberá generar también un AFD directamente de la expresión regular r. Con los autómatas generados deberá determinar si 𝑤 ∈ 𝐿(𝑟).

Especificación del funcionamiento del programa
● Entrada
    o Una expresión regular 𝑟 .
    o Una cadena 𝑤 a ser validada. 
● Salida
    o Por cada AF (Autómata Finito) generado a partir de 𝑟 , es decir, por cada AFD y AFN generado:
        ▪ El programa debe indicar si 𝑤 ∈ 𝐿(𝑟) con un “sí” en caso el enunciado anterior sea correcto, de lo contrario deberá mostrar un “no”.
        ▪ Además, deberá generar como output adicional una imagen con el Grafo correspondiente para el AF generado, mostrando el estado inicial, los estados adicionales, el estado de aceptación y las transiciones con sus símbolos correspondientes.
"""
###### ----> Ejemplos del pre-lab
# print(infixToPostfix('ab ∗ ab ∗'))
# print(infixToPostfix('0? (1? )? 0 ∗')) 
# print(infixToPostfix('(a*|b*)c')) 
# print(infixToPostfix('(b|b)*abb(a|b)*')) 
# print(infixToPostfix('(a|ε)b(a+)c?'))
# print(infixToPostfix('(a|b)*a(a|b)(a|b)'))


# Importamos las librerías necesarias.
from validations import *
from reToPosfix import infixToPostfix
from thompsonAlgorithm import thompsonBuild
from showNFA import drawNFA


# Pedimos la expresión regular (regex) al usuario.
r = input("\nIngrese la expresión regular: ")
print('-----------------------------------------')

# Validamos la expresión regular
# Si es válida, se procede a convertirla a notación posfija
# Si no es válida, se muestra un mensaje de error
if checkForErrors(r) == []:
    print('La expresión regular es válida')
    print('-----------------------------------------')
    postfixExp = infixToPostfix(r)
    print('La expresión regular en notación posfija es: ', postfixExp)
    print('-----------------------------------------')
    # Si el regex es válido, se procede a construir el AFN
    print('El AFN construido es: ')
    nfaBuilt = thompsonBuild(postfixExp)
    print('-----------------------------------------')
    print('Mostrando el NFA...')
    # Mostramos el AFN
    drawNFA(nfaBuilt)

else:
    print('La expresión regular es inválida')
    print('-----------------------------------------')
    print('Errores encontrados: ')
    for error in checkForErrors(r):
        print(error)