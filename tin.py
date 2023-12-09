import numpy as np
from classes import Nodo
import copy
import random

#creacion del tablero principal
matriz = np.array([[1,1,0,0,0,0,1,1],
                  [1,0,0,0,0,0,0,1],
                  [0,0,0,0,0,0,0,0],
                  [3,0,0,2,2,0,0,0],
                  [0,0,0,2,2,0,0,0],
                  [0,0,0,0,0,4,0,0],
                  [1,0,0,0,0,0,0,1],
                  [1,1,0,0,0,0,1,1]])

#encuentra la posicion de un objeto en un tablero de acuerdo a su id
def Encontrar_Posicion(id,tablero):
  lista_posiciones = []
  for i, fila in enumerate(tablero):
    for j, columna in enumerate(fila):
      if columna == id:
        lista_posiciones.append((i,j))
  
  return lista_posiciones

posicion_M = Encontrar_Posicion(3,matriz)
posicion_J = Encontrar_Posicion(4,matriz)
posicion_Monedas = Encontrar_Posicion(1,matriz)
posicion_Especiales = Encontrar_Posicion(2,matriz)

#con esto se controla el listado de posiciones disponibles para los jugadores
posiciones_No_Accesibles = []

#se crea el nodo padre que seria cuando el juego comienza con:
    #Turno = Maquina = 3
    #Tablero = matriz
    #valor = 0 = heuristica
    #posicion = posicionMaquina
    #contrincante = posicionjugador
nodo_inicial = Nodo(3, matriz,0, posicion_M,posicion_J,posiciones_No_Accesibles)

#posiblesmovimientos verifica que movimientos puede realizar el jugador
#retorna una lista de los mismos

def Posibles_Movimientos(nodo):
  OchoPosibles =[(-2,1),(-1,2),(1,2),(2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
  Movimientos = []  
  for posible in OchoPosibles:

    posible_x = nodo.posicion[0][0] + posible[0]
    posible_y = nodo.posicion[0][1] + posible[1]

    if (posible_x <= 7 and posible_x >= 0 and
    posible_y <= 7 and posible_y >= 0 and 
    (posible_x,posible_y) != (nodo.posicion_Contrincante[0][0],nodo.posicion_Contrincante[0][1])):

        if (posible_x,posible_y) not in nodo.Cerrados:
            Movimientos.append((posible_x,posible_y))

  return Movimientos

#realizar movimiento cambia el estado del tablero
def realizar_movimiento(tablero, nueva_posicion, posicion, jugador, Cerrados):
    nuevo_tablero = copy.deepcopy(tablero)
    nuevo_cerrado = copy.deepcopy(Cerrados)
    nuevo_valor = 0

    # Aquí se controla todo lo que pasa cuando el jugador/Maquina mueve una posición en el tablero
    nuevo_tablero[nueva_posicion[0]][nueva_posicion[1]] = jugador
    nuevo_tablero[posicion[0][0]][posicion[0][1]] = 0

    if nueva_posicion in posicion_Monedas:
        nuevo_cerrado.append(nueva_posicion)
        if jugador == 3:
            nuevo_valor += 1
    elif nueva_posicion in posicion_Especiales:
        nuevo_cerrado.append(nueva_posicion)
        if jugador == 3:
            nuevo_valor += 3

    # Actualiza el valor acumulado del movimiento actual
    nuevo_valor += nuevo_valor

    return nuevo_tablero, nuevo_cerrado, nuevo_valor

#cambiar turno controla quien debera jugar ahora
def cambiar_turno(jugador):
    if jugador == 3:
        return 4
    else:return 3

#generarArbol, crea el arbol con profundidad maxima que será el que observa la maquina
def generarArbol(nodo, profundidadMax, profundidad=0):
    if profundidad == profundidadMax:
        return nodo

    posiciones_hijos = Posibles_Movimientos(nodo)

    for nueva_posicion in posiciones_hijos:
        nuevo_tablero, nuevo_cerrado, nuevo_valor = realizar_movimiento(
            nodo.tablero, nueva_posicion, nodo.posicion, nodo.jugador, nodo.Cerrados)
        nuevo_valor += profundidad
        nuevo_nodo = Nodo(cambiar_turno(nodo.jugador), nuevo_tablero, nuevo_valor,
                         Encontrar_Posicion(cambiar_turno(nodo.jugador), nuevo_tablero),
                         Encontrar_Posicion(nodo.jugador, nuevo_tablero), nuevo_cerrado)
        nodo.hijos.append(nuevo_nodo)
        generarArbol(nuevo_nodo, profundidadMax, profundidad=profundidad + 1)

    return nodo


def MiniMax(nodo, Maximiza, alfa, beta):
    if not nodo.hijos:
        return nodo.valor

    if Maximiza:
        valor = float("-inf")
        for hijo in nodo.hijos:
            valor = max(valor, MiniMax(hijo, False, alfa, beta))
            alfa = max(alfa, valor)

            if beta <= alfa:
                break

        nodo.valor = valor
        return valor + nodo.profundidad  # Agrega la profundidad al valor

    else:
        valor = float("inf")
        for hijo in nodo.hijos:
            valor = min(valor, MiniMax(hijo, True, alfa, beta))
            beta = min(beta, valor)

            if beta <= alfa:
                break

        nodo.valor = valor
        return valor + nodo.profundidad  # Agrega la profundidad al valor

# def Mejor_movimiento(nodo):
#     #falta usar el minimax para que retorne el mejor movimiento
#     mejor_valor = float("-inf")
#     mejor_movimiento = None
#     alfa = float("-inf")
#     beta = float("inf")

#     for hijo in nodo.hijos:
#         valor = MiniMax(hijo, False, alfa, beta)
#         if valor > mejor_valor:
#             mejor_valor = valor
#             mejor_movimiento = hijo
#         alfa = max(alfa, mejor_valor)

#     return mejor_movimiento

# def guardarValorNodo(nodo):
#     # mejor_nodo = Mejor_movimiento(nodo)
#     # mejor_nodo.valor = mejor_nodo.profundidad
#     nodo.valor = nodo.profundidad
#   return mejor_nodo.valor

def imprimir_arbol(nodo, nivel=0, desplazamiento=2):
    if nodo is not None:
        # Agregar desplazamiento a la información de cada nodo
        desplazamiento_actual = desplazamiento * nivel

        print(" " * 2*desplazamiento_actual + f"Jugador: {nodo.jugador}")
        if nodo.valor is not None:
            print(" " *2* desplazamiento_actual + f"Valor: {nodo.valor}")
        if nodo.Cerrados is not None:
            print(" " * 2*desplazamiento_actual + f"No_Accesibles: {nodo.Cerrados}")
        if nodo.posicion is not None:
            print(" " *2* desplazamiento_actual + f"Posición: {nodo.posicion}")
        if nodo.tablero is not None:
            print(" " * 2*desplazamiento_actual + "Tablero:")
            for fila in nodo.tablero:
                print(" " *2* desplazamiento_actual + str(fila))
        print("-" * 40)
        for hijo in nodo.hijos:
            imprimir_arbol(hijo, nivel + 1, desplazamiento)

arbol = generarArbol(nodo_inicial,2)
imprimir_arbol(arbol)



#print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
#imprimir_arbol(Mejor_movimiento(arbol))

# print(MiniMax(arbol,True,float("-inf"),float("inf")))
# print("mejor movimiento")
# print(Mejor_movimiento(arbol).valor)
# print(Mejor_movimiento(arbol).tablero)


#  crear archivo guarda el arbol en un archivo txt
def crear_archivo(nodo, nivel=0, desplazamiento=2):
    if nodo is not None:
        # Agregar desplazamiento a la información de cada nodo
        desplazamiento_actual = desplazamiento * nivel

        archivo.write(" " * 2*desplazamiento_actual + f"Jugador: {nodo.jugador}\n")
        if nodo.valor is not None:
            archivo.write(" " *2* desplazamiento_actual + f"Valor: {nodo.valor}\n")
        if nodo.Cerrados is not None:
            archivo.write(" " * 2*desplazamiento_actual + f"No_Accesibles: {nodo.Cerrados}\n")
        if nodo.posicion is not None:
            archivo.write(" " *2* desplazamiento_actual + f"Posición: {nodo.posicion}\n")
        if nodo.tablero is not None:
            archivo.write(" " * 2*desplazamiento_actual + "Tablero:\n")
            for fila in nodo.tablero:
                archivo.write(" " *2* desplazamiento_actual + str(fila) + "\n")
        archivo.write("-" * 40 + "\n")
        for hijo in nodo.hijos:
            crear_archivo(hijo, nivel, desplazamiento)

archivo = open("arbol.txt","w")
crear_archivo(arbol)
archivo.close()
