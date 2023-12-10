
class Nodo:
    valor = None
    
    def  __init__(self,posicion_J1, posicion_J2, puntos_J1, puntos_J2,monedas,monedasEspeciales,posicionesBloqueadas, tipoNodo, profundidad = 0, padre = None, hijos = None):
        self.posicion_J1 = posicion_J1
        self.posicion_J2 = posicion_J2
        self.puntos_J1 = puntos_J1
        self.puntos_J2 = puntos_J2
        self.monedas = monedas
        self.monedasEspeciales = monedasEspeciales
        self.posicionesBloqueadas = posicionesBloqueadas
        self.tipoNodo = tipoNodo
        self.profundidad = profundidad
        self.padre = padre
        self.hijos = hijos if hijos is not None else []
        
        if tipoNodo == "Max":
            self.valor = float("-inf")
        elif tipoNodo == "Min":
            self.valor == float("inf")



