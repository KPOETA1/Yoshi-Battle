
class Nodo:

    def  __init__(self, jugador,tablero,valor, posicion,posicion_Contrincante,Cerrados,hijos = None):
        self.valor = valor
        self.posicion = posicion
        self.posicion_Contrincante = posicion_Contrincante
        self.jugador = jugador
        self.tablero = tablero
        self.Cerrados = Cerrados
        self.hijos = []


