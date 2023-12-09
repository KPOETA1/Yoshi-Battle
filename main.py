import numpy as np
from classes import Nodo
import copy
import random

#creacion del tablero principal
matriz = np.array([[1,1,0,0,0,0,1,1],
                  [1,0,0,0,0,0,0,1],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,2,2,0,4,0],
                  [0,0,0,2,2,0,0,0],
                  [0,0,0,0,0,3,0,0],
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
def realizar_movimiento(tablero,nueva_posicion,posicion, jugador, Cerrados):
    nuevo_tablero = copy.deepcopy(tablero)
    nuevo_cerrado  = copy.deepcopy(Cerrados)
     #aqui se controla todo lo que pasa cuando el jugador/Maquina mueve una posicion en el tablero

    nuevo_tablero[nueva_posicion[0]][nueva_posicion[1]] = jugador
    nuevo_tablero[posicion[0][0]][posicion[0][1]] = 0
    
    if nueva_posicion in posicion_Monedas or nueva_posicion in posicion_Especiales:
        nuevo_cerrado.append(nueva_posicion)

    return nuevo_tablero,nuevo_cerrado
   

#cambiar turno controla quien debera jugar ahora
def cambiar_turno(jugador):
    if jugador == 3:
        return 4
    else:return 3

#generarArbol, crea el arbol con profundidad maxima que será el que observa la maquina
def generarArbol(nodo, profundidadMax, profundidad = 0):
    if profundidad == profundidadMax:
        nodo.valor = random.randint(1, 9)
        return nodo
    
    posiciones_hijos = Posibles_Movimientos(nodo)

    for nueva_posicion in posiciones_hijos:
        nuevo_tablero, nuevo_cerrado = realizar_movimiento(nodo.tablero, nueva_posicion,nodo.posicion, nodo.jugador,nodo.Cerrados)
        nuevo_nodo = Nodo(cambiar_turno(nodo.jugador),nuevo_tablero,None,Encontrar_Posicion(cambiar_turno(nodo.jugador),
                nuevo_tablero),Encontrar_Posicion(nodo.jugador,nuevo_tablero),nuevo_cerrado)
        nodo.hijos.append(nuevo_nodo)
        generarArbol(nuevo_nodo,profundidadMax,profundidad + 1)

    return nodo


def MiniMax(nodo,Maximiza, alfa,beta):
    if not nodo.hijos:
        return nodo.valor #si se llega a un nodo terminal, se retorna el valor de la heuristica

    if Maximiza: #algoritmo si se esta maximizando
        valor = float("-inf")
        for hijo in nodo.hijos: #se ve el valor de max para cada hijo del nodo, siempre y cuando beta>=alfa
            valor = max(valor,MiniMax(hijo,False,alfa,beta))
            alfa = max(alfa,valor)

            if beta <= alfa:
                break #podar
        nodo.valor = valor

        return valor

    else: #algoritmo si esta minimizando
        valor = float("inf")
        for hijo in nodo.hijos: #se ve el valor de min para cada hijo del nodo, siempre y cuando beta>=alfa
            valor = min(valor,MiniMax(hijo,True,alfa,beta))
            beta = min(beta,valor)

            if beta <= alfa:
                break #podar

        nodo.valor = valor
        
        return valor

def Mejor_movimiento(nodo):
    #falta usar el minimax para que retorne el mejor movimiento
    mejor_valor = float("-inf")
    mejor_movimiento = None
    alfa = float("-inf")
    beta = float("inf")

    for hijo in nodo.hijos:
        valor = MiniMax(hijo, False, alfa, beta)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = hijo
        alfa = max(alfa, mejor_valor)

    return mejor_movimiento

    
def imprimir_arbol(nodo, nivel=0, desplazamiento=2):
    if nodo is not None:
        # Agregar desplazamiento a la información de cada nodo
        desplazamiento_actual = desplazamiento * nivel

        print(" " * 2*desplazamiento_actual + f"Jugador: {nodo.jugador}")
        if nodo.valor is not None:
            print(" " *2* desplazamiento_actual + f"Costo: {nodo.valor}")
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

print(MiniMax(arbol,True,float("-inf"),float("inf")))
print("mejor movimiento")
print(Mejor_movimiento(arbol).valor)
print(Mejor_movimiento(arbol).tablero)

