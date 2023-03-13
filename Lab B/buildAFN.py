"""
Este módulo contiene las clases necesarias para 
construir un AFN a partir de una expresión regular
"""

class Transition:
    """
    Representa una transición entre estados en el NFA 
    -> donde start_state es el estado de origen 
    -> symbol es el símbolo que activa la transición 
    -> accept_state es el estado de destino
    
    Los métodos start y accept son para establecer el estado de origen y destino de la transición
    """
    def __init__(self, start_state, symbol, accept_state):
        self.start_state = start_state
        self.symbol = symbol
        self.accept_state = accept_state

    def start(self, start_state):
        self.start_state = start_state

    def accept(self, accept_state):
        self.accept_state = accept_state

class State:
    """
    Representa un estado en el NFA
    -> donde label es una etiqueta opcional para el estado 
    -> accept indica si el estado es un estado de aceptación 
        si el NFA acepta una cadena de entrada si termina en este estado
    """
    def __init__(self, label=None):
        self.label = label
        self.accept = False

class NFA:
    """
    Representa el NFA:
    -> donde q es el conjunto de estados
    -> expr es una expresión regular que define el lenguaje aceptado por el NFA
    -> alphabet es el alfabeto del lenguaje
    -> q0 es el estado inicial
    -> f es el conjunto de estados de aceptación 
    -> transitions es el conjunto de transiciones entre estados
    """
    def __init__(self, q, expr, alphabet, q0, f, transitions):
        self.q = q
        self.expr = expr
        self.alphabet = alphabet
        self.q0 = q0
        self.f = f
        self.transitions = transitions

