from classes import Nodo
from copy import deepcopy


def crearArbol(nodo,profundidad):
    if profundidad == 0:
        return None

    if nodo.tipoNodo == "Max":
        listaMovimientos = posiblesMovimientos(nodo.posicion_J1,nodo.posicion_J2)

        for movimiento in listaMovimientos:
            monedasCopia = deepcopy(nodo.monedas)
            monedasEspecialesCopia = deepcopy(nodo.monedasEspeciales)
            posicionesBloqueadasCopia = deepcopy(nodo.posicionesBloqueadas)

            puntos = verificarMovimiento(movimiento,nodo.monedas,nodo.monedasEspeciales)

            nuevaPosicion = movimiento
            
            if puntos:
                if puntos == 1:
                    monedasCopia.remove(movimiento)
                if puntos == 3:
                    monedasEspecialesCopia.remove(movimiento)
                posicionesBloqueadasCopia.append(movimiento)

                puntos_J1 = nodo.puntos_J1 + escalarPuntos(puntos,nodo.profundidad)
            else:
                puntos_J1 = nodo.puntos_J1

            nuevoNodo = Nodo(
                posicion_J1 = nuevaPosicion,
                posicion_J2 = nodo.posicion_J2,
                puntos_J1 = puntos_J1,
                puntos_J2 = nodo.puntos_J2,
                monedas = monedasCopia,
                monedasEspeciales = monedasEspecialesCopia,
                posicionesBloqueadas = posicionesBloqueadasCopia,
                tipoNodo = "Min",
                profundidad = nodo.profundidad + 1,
                padre = nodo
            )
            nodo.hijos.append(nuevoNodo)
            crearArbol(nuevoNodo,profundidad -1)

    elif nodo.tipoNodo == "Min":
        listaMovimientos = posiblesMovimientos(nodo.posicion_J2,nodo.posicion_J1)

        for movimiento in listaMovimientos:
            monedasCopia = deepcopy(nodo.monedas)
            monedasEspecialesCopia = deepcopy(nodo.monedasEspeciales)
            posicionesBloqueadasCopia = deepcopy(nodo.posicionesBloqueadas)

            puntos = verificarMovimiento(movimiento,nodo.monedas,nodo.monedasEspeciales)

            nuevaPosicion = movimiento
            
            if puntos:
                if puntos == 1:
                    monedasCopia.remove(movimiento)
                if puntos == 3:
                    monedasEspecialesCopia.remove(movimiento)
                posicionesBloqueadasCopia.append(movimiento)

                puntos_J2 = nodo.puntos_J2 + escalarPuntos(puntos,nodo.profundidad)
            else:
                puntos_J2 = nodo.puntos_J2

            nuevoNodo = Nodo(
                posicion_J1 = nodo.posicion_J1,
                posicion_J2 = nuevaPosicion,
                puntos_J1 = nodo.puntos_J1,
                puntos_J2 = puntos_J2,
                monedas = monedasCopia,
                monedasEspeciales = monedasEspecialesCopia,
                posicionesBloqueadas = posicionesBloqueadasCopia,
                tipoNodo = "Max",
                profundidad = nodo.profundidad + 1,
                padre = nodo
            )
            nodo.hijos.append(nuevoNodo)
            crearArbol(nuevoNodo, profundidad -1)

#priorizar que siempre se agarren puntos
def escalarPuntos(puntos, profundidad):
    return puntos


def verificarMovimiento(movimiento,monedas,monedasEspeciales):
    if movimiento in monedas:
        return 1
    if movimiento in monedasEspeciales:
        return 3
    return None


def posiblesMovimientos(posicionActual,posicionRival,posicionesBloqueadas):
  ochoPosibles =[(-2,1),(-1,2),(1,2),(2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
  movimientos = []  
  for posible in ochoPosibles:

    posibleX = posicionActual[0] + posible[0]
    posibleY = posicionActual[1] + posible[1]

    if (posibleX <= 7 and posibleX >= 0 and
    posibleY <= 7 and posibleY >= 0 and 
    (posibleX,posibleY) != (posicionRival[0],posicionRival[1])): 

        if (posibleX,posibleY) not in posicionesBloqueadas:
            movimientos.append((posibleX,posibleY))

    return movimientos

monedasPrueba = []


if __name__ == "__main__":
    nodo = Nodo()

