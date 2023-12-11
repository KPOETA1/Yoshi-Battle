from classes import Nodo
from copy import deepcopy
import pygame as pyg


def crearArbol(nodo, profundidad):
    if profundidad == 0:
        return None

    if nodo.tipoNodo == "Max":
        listaMovimientos = posiblesMovimientos(nodo.posicion_J1, nodo.posicion_J2, nodo.posicionesBloqueadas)

        for movimiento in listaMovimientos:
            pyg.event.pump()
            monedasCopia = deepcopy(nodo.monedas)
            monedasEspecialesCopia = deepcopy(nodo.monedasEspeciales)
            posicionesBloqueadasCopia = deepcopy(nodo.posicionesBloqueadas)

            puntos = verificarMovimiento(movimiento, nodo.monedas, nodo.monedasEspeciales)

            nuevaPosicion = movimiento

            if puntos:
                if puntos == 1:
                    monedasCopia.remove(movimiento)
                if puntos == 3:
                    monedasEspecialesCopia.remove(movimiento)
                posicionesBloqueadasCopia.append(movimiento)

                puntos_J1 = nodo.puntos_J1 + escalarPuntos(puntos, nodo.profundidad)
            else:
                puntos_J1 = nodo.puntos_J1

            nuevoNodo = Nodo(
                posicion_J1=nuevaPosicion,
                posicion_J2=nodo.posicion_J2,
                puntos_J1=puntos_J1,
                puntos_J2=nodo.puntos_J2,
                monedas=monedasCopia,
                monedasEspeciales=monedasEspecialesCopia,
                posicionesBloqueadas=posicionesBloqueadasCopia,
                tipoNodo="Min",
                profundidad=nodo.profundidad + 1,
                padre=nodo
            )
            nodo.hijos.append(nuevoNodo)
            crearArbol(nuevoNodo, profundidad - 1)

    elif nodo.tipoNodo == "Min":
        listaMovimientos = posiblesMovimientos(nodo.posicion_J2, nodo.posicion_J1, nodo.posicionesBloqueadas)

        for movimiento in listaMovimientos:
            pyg.event.pump()
            monedasCopia = deepcopy(nodo.monedas)
            monedasEspecialesCopia = deepcopy(nodo.monedasEspeciales)
            posicionesBloqueadasCopia = deepcopy(nodo.posicionesBloqueadas)

            puntos = verificarMovimiento(movimiento, nodo.monedas, nodo.monedasEspeciales)

            nuevaPosicion = movimiento

            if puntos:
                if puntos == 1:
                    monedasCopia.remove(movimiento)
                if puntos == 3:
                    monedasEspecialesCopia.remove(movimiento)
                posicionesBloqueadasCopia.append(movimiento)

                puntos_J2 = nodo.puntos_J2 + escalarPuntos(puntos, nodo.profundidad)
            else:
                puntos_J2 = nodo.puntos_J2

            nuevoNodo = Nodo(
                posicion_J1=nodo.posicion_J1,
                posicion_J2=nuevaPosicion,
                puntos_J1=nodo.puntos_J1,
                puntos_J2=puntos_J2,
                monedas=monedasCopia,
                monedasEspeciales=monedasEspecialesCopia,
                posicionesBloqueadas=posicionesBloqueadasCopia,
                tipoNodo="Max",
                profundidad=nodo.profundidad + 1,
                padre=nodo
            )
            nodo.hijos.append(nuevoNodo)
            crearArbol(nuevoNodo, profundidad - 1)


# priorizar que siempre se agarren puntos
def escalarPuntos(puntos, profundidad):
    # if profundidad == 0:
    #     return 0
    # if profundidad == 1 or profundidad == 2:
    #     return puntos
    # if profundidad == 3 or profundidad == 4:
    #     return puntos * 0.7
    # if profundidad == 5 or profundidad == 6:
    #     return puntos * 0.4
    return puntos


def verificarMovimiento(movimiento, monedas, monedasEspeciales):
    if movimiento in monedas:
        return 1
    if movimiento in monedasEspeciales:
        return 3
    return None


def posiblesMovimientos(posicionActual, posicionRival, posicionesBloqueadas):
    ochoPosibles = [(-2, 1), (-1, 2), (1, 2), (2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
    movimientos = []

    for posible in ochoPosibles:
        pyg.event.pump()
        posibleX = posicionActual[0] + posible[0]
        posibleY = posicionActual[1] + posible[1]

        if (posibleX <= 7 and posibleX >= 0 and
                posibleY <= 7 and posibleY >= 0 and
                (posibleX, posibleY) != (posicionRival[0], posicionRival[1])):

            if (posibleX, posibleY) not in posicionesBloqueadas:
                movimientos.append((posibleX, posibleY))

    return movimientos


def nodoALista(nodo):
    lista = []

    for hijo in nodo.hijos:
        pyg.event.pump()
        lista.append(hijo)
        lista += nodoALista(hijo)

    return lista


def actualizarArbol(arbol):
    hijos = nodoALista(arbol)
    profundidadArbol = 0

    for hijo in hijos:
        pyg.event.pump()
        if hijo.profundidad > profundidadArbol:
            profundidadArbol = hijo.profundidad

    for hijo in hijos:
        pyg.event.pump()
        hijo.valor = hijo.puntos_J1 - hijo.puntos_J2 + heuristica(hijo, hijo.monedas, hijo.monedasEspeciales)

    while profundidadArbol > 0:
        for hijo in hijos:
            pyg.event.pump()
            if hijo.profundidad == profundidadArbol:
                if hijo.padre.tipoNodo == "Max":
                    hijo.padre.valor = max(hijo.padre.valor, hijo.valor)
                elif hijo.padre.tipoNodo == "Min":
                    hijo.padre.valor = min(hijo.padre.valor, hijo.valor)
        profundidadArbol -= 1


def minimax(posicion_J1, posicion_J2, puntos_J1, puntos_J2, monedas, monedasEspeciales, posicionesBloqueadas,
            profundidad):
    nodo = Nodo(
        posicion_J1=posicion_J1,
        posicion_J2=posicion_J2,
        puntos_J1=puntos_J1,
        puntos_J2=puntos_J2,
        monedas=monedas,
        monedasEspeciales=monedasEspeciales,
        posicionesBloqueadas=posicionesBloqueadas,
        tipoNodo="Max",
        profundidad=0,
        padre=None
    )

    crearArbol(nodo, profundidad)

    print("Root: ", nodo.posicion_J1, nodo.posicion_J2, nodo.tipoNodo, "-depth", nodo.profundidad, '-node_score', nodo.puntos_J1+nodo.puntos_J2)
    children = nodoALista(nodo)
    for child in children:
        print(
            child.tipoNodo, 
            "-depth", child.profundidad,
            "-j1:", 
            child.posicion_J1, 
            child.puntos_J1,
            "-j2:", 
            child.posicion_J2, 
            child.puntos_J2,
            )

    actualizarArbol(nodo)

    for hijo in nodo.hijos:
        pyg.event.pump()
        if hijo.valor == nodo.valor and hijo.profundidad == 1:
            return hijo.posicion_J1


def movValido(x, y):
    # Funcion auxiliar para verificar si una posicion (x,y) esta dentro del tablero de 8x8
    return 0 <= x < 8 and 0 <= y < 8


def manhattan(inicial, destino):
    #Funcion auxiliar para calcular la distancia manhattan entre dos posiciones
    return abs(inicial[0] - destino[0]) + abs(inicial[1] - destino[1])

def nroMovimientos(posInicial, posDestino):
    #Diccionario que relaciona la distancia manhattan entre 2 puntos y la cantidad de movimientos que se necesitan para llegar de un punto a otro
    #Clave: distancia manhattan
    #Valor: cantidad de movimientos
    distancias = {
        0: 1,
        1: 3,
        2: 2,
        3: 3,
        4: 4,
        5: 3,
        6: 4,
        7: 5,
        8: 4,
        9: 5,
        10: 4,
        11: 5,
        12: 4,
        13: 5,
        14: 6
    }

    #nroMovimientos para el jugador
    manhattanActual = manhattan(posInicial, posDestino)
    if manhattan == 3:
        movimientosPosibles = posiblesMovimientos(posInicial, (20,20), [])
        if posDestino in movimientosPosibles:
            return 1
        else:
            return distancias[manhattanActual]
    elif posInicial == (0,0) or posInicial == (0,7) or posInicial == (7,0) or posInicial == (7,7):
        if manhattanActual == 2:
            return distancias[4]
        else:
            return distancias[manhattanActual]
    else:
        return distancias[manhattanActual]


def heuristica(nodo, monedas, monedasEspeciales):
    # Funcion heuristica para calcular el valor de un nodo
    valorUtilidad = 0

    # Calcular la distancia minima desde la posicion del jugador 1 hasta cada moneda
    for moneda in monedas:
        pyg.event.pump()
        if moneda == 0:
            None
        else:
            valorUtilidad += 1 / nroMovimientos(nodo.posicion_J1, moneda)

    # Calcular la distancia minima desde la posicion del jugador 1 hasta cada moneda especial
    for monedaEspecial in monedasEspeciales:
        pyg.event.pump()
        if monedaEspecial == 0:
            None
        else:
            valorUtilidad += 3 / nroMovimientos(nodo.posicion_J1, monedaEspecial)

    # Calcular la distancia minima desde la posicion del jugador 2 hasta cada moneda
    for moneda in monedas:
        pyg.event.pump()
        if moneda == 0:
            None
        else:
            valorUtilidad -= 1 / nroMovimientos(nodo.posicion_J2, moneda)

    # Calcular la distancia minima desde la posicion del jugador 2 hasta cada moneda especial
    for monedaEspecial in monedasEspeciales:
        pyg.event.pump()
        if monedaEspecial == 0:
            None
        else:
            valorUtilidad -= 3 / nroMovimientos(nodo.posicion_J2, monedaEspecial)

    return valorUtilidad


if __name__ == "__main__":
    monedasPrueba = [(0, 0), (0, 1), (0, 6), (0, 7), (1, 0), (1, 7), (6, 0), (6, 7), (7, 0), (7, 1), (7, 6), (7, 7)]
    monedasEspecialesPrueba = [(3, 3), (3, 4), (4, 3), (4, 4)]

    nodo = Nodo(
        posicion_J1=(2, 2),
        posicion_J2=(5, 5),
        puntos_J1=0,
        puntos_J2=0,
        monedas=monedasPrueba,
        monedasEspeciales=monedasEspecialesPrueba,
        posicionesBloqueadas=[],
        tipoNodo="Max",
        profundidad=0,
        padre=None
    )

    print(heuristica(nodo, nodo.monedas, nodo.monedasEspeciales))

    posicion = minimax(nodo.posicion_J1, nodo.posicion_J2, nodo.puntos_J1, nodo.puntos_J2, nodo.monedas,
                       nodo.monedasEspeciales, nodo.posicionesBloqueadas, 2)

    # print(posicion)