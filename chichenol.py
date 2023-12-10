from classes import Nodo
from copy import deepcopy


def crearArbol(nodo, profundidad):
    if profundidad == 0:
        return None

    if nodo.tipoNodo == "Max":
        listaMovimientos = posiblesMovimientos(nodo.posicion_J1, nodo.posicion_J2, nodo.posicionesBloqueadas)

        for movimiento in listaMovimientos:
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
        lista.append(hijo)
        lista += nodoALista(hijo)

    return lista


def actualizarArbol(arbol):
    hijos = nodoALista(arbol)
    profundidadArbol = 0

    for hijo in hijos:
        if hijo.profundidad > profundidadArbol:
            profundidadArbol = hijo.profundidad

    for hijo in hijos:
        hijo.valor = hijo.puntos_J1 - hijo.puntos_J2 + heuristica(hijo)

    while profundidadArbol > 0:
        for hijo in hijos:
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
        if hijo.valor == nodo.valor and hijo.profundidad == 1:
            return hijo.posicion_J1


def heuristica(nodo):
    return 0


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

    posicion = minimax(nodo.posicion_J1, nodo.posicion_J2, nodo.puntos_J1, nodo.puntos_J2, nodo.monedas,
                       nodo.monedasEspeciales, nodo.posicionesBloqueadas, 2)

    print(posicion)