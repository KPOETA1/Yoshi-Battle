# classes.py

class Nodo:

    def  __init__(self, jugador,tablero,valor,profundidad, posicion,posicion_Contrincante,Cerrados,hijos = None):
        self.valor = valor
        self.profundidad = profundidad
        self.posicion = posicion
        self.posicion_Contrincante = posicion_Contrincante
        self.jugador = jugador
        self.tablero = tablero
        self.Cerrados = Cerrados
        self.hijos = []


