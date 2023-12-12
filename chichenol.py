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

    actualizarArbol(nodo)

    for hijo in nodo.hijos:
        pyg.event.pump()
        if hijo.valor == nodo.valor and hijo.profundidad == 1:
            return hijo.posicion_J1


def movValido(x, y):
    # Funcion auxiliar para verificar si una posicion (x,y) esta dentro del tablero de 8x8
    return 0 <= x < 8 and 0 <= y < 8


def nroMovimientos(posicionInicial, posicionObjetivo):
    '''
    Calcula la cantidad minima de movimientos que un caballo necesita para llegar de posInicial a posObjetivo en un tablero de 8x8
    '''
    # Definir posiciones relativas de los movimientos del caballo
    movimientosCaballo = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    # Desempaquetar posiciones iniciales y objetivos
    xInicial, yInicial = posicionInicial
    xObjetivo, yObjetivo = posicionObjetivo

    # Verificar si las posiciones iniciales y objetivos son validas
    if not movValido(xInicial, yInicial) or not movValido(xObjetivo, yObjetivo):
        print("Posiciones fuera del Tablero.")

    # # Inicializar un diccionario para almacenar la distancia minima desde la posicion inicial hasta cada posicion en el tablero
    # distancia = {(i, j): float('inf')for i in range(8) for j in range(8)}
    #
    # # La distancia desde la posicion inicial hasta si misma es 0
    # distancia[posicionInicial] = 0
    #
    # # Implementar BFS (Breadth-First Search) para calcular la distancia minima
    # cola = [posicionInicial]
    # padres = {posicionInicial: None}
    #
    # while cola:
    #     xActual, yActual = cola.pop(0)
    #
    #     for dx, dy in movimientosCaballo:
    #         pyg.event.pump()
    #         xNuevo, yNuevo = xActual + dx, yActual + dy
    #
    #         if movValido(xNuevo, yNuevo) and distancia[(xNuevo, yNuevo)] == float('inf'):
    #             distancia[(xNuevo, yNuevo)] = distancia[(xActual, yActual)] + 1
    #             cola.append((xNuevo, yNuevo))
    #             padres[(xNuevo, yNuevo)] = (xActual, yActual)
    #
    # # Devolver la distancia minima hasta la posicion objetivo
    # return distancia[posicionObjetivo]

    dx = abs(xInicial - xObjetivo)
    dy = abs(yInicial - yObjetivo)

    # Aplicar la fórmula de la distancia Manhattan en L
    distancia_L = max(dx, dy) + min(dx, dy)

    return distancia_L


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