import numpy as np
from classes import Nodo
import copy
import random
import sys

#creacion del tablero principal
matriz = np.array([[1,1,0,0,0,0,1,1],
                  [1,0,0,0,0,0,0,1],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,2,2,0,0,0],
                  [0,0,0,2,2,0,0,0],
                  [0,0,0,0,0,0,0,0],
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

#  def lista de posiciones en 0 en el tablero
def Encontrar_Posicion_0(tablero):
  lista_posiciones = []
  for i, fila in enumerate(tablero):
    for j, columna in enumerate(fila):
      if columna == 0:
        lista_posiciones.append((i,j))
  
  return lista_posiciones

def actualizar_matriz(matriz, posicion_M, posicion_J):
    matriz[posicion_M[0]][posicion_M[1]] = 3
    matriz[posicion_J[0]][posicion_J[1]] = 4

    return matriz


posiciones_vacias = Encontrar_Posicion_0(matriz)
posicion_M = random.choice(posiciones_vacias)
print(posicion_M)
posicion_J = random.choice(posiciones_vacias)
print(posicion_J)

posicion_Monedas = Encontrar_Posicion(1,matriz)
posicion_Especiales = Encontrar_Posicion(2,matriz)

# Asegurarse de que las posiciones sean diferentes
while posicion_M == posicion_J:
    posicion_J = random.choice(posiciones_vacias)

#con esto se controla el listado de posiciones disponibles para los jugadores
posiciones_No_Accesibles = []

matriz = actualizar_matriz(matriz, posicion_M, posicion_J)

#se crea el nodo padre que seria cuando el juego comienza con:
    #Turno = Maquina = 3
    #Tablero = matriz
    #valor = 0 = heuristica
    #posicion = posicionMaquina
    #contrincante = posicionjugador
nodo_inicial = Nodo(3, matriz, 0, 0, [posicion_M], [posicion_J], posiciones_No_Accesibles)

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
    nuevo_valor = 0
     #aqui se controla todo lo que pasa cuando el jugador/Maquina mueve una posicion en el tablero

    nuevo_tablero[nueva_posicion[0]][nueva_posicion[1]] = jugador
    nuevo_tablero[posicion[0][0]][posicion[0][1]] = 0
    
    if nueva_posicion in posicion_Monedas :
        nuevo_cerrado.append(nueva_posicion)
        if jugador == 3:
            nuevo_valor += 1
    elif nueva_posicion in posicion_Especiales:
        nuevo_cerrado.append(nueva_posicion)
        if jugador == 3:
            nuevo_valor += 3

    return nuevo_tablero,nuevo_cerrado,nuevo_valor
   

#cambiar turno controla quien debera jugar ahora
def cambiar_turno(jugador):
    if jugador == 3:
        return 4
    else:return 3

#generarArbol, crea el arbol con profundidad maxima que será el que observa la maquina
def generarArbol(nodo, profundidadMax, profundidad = 0):
    if profundidad == profundidadMax:
        #nodo.valor = random.randint(1, 9)
        return nodo
    
    posiciones_hijos = Posibles_Movimientos(nodo)

    for nueva_posicion in posiciones_hijos:
        
        nuevo_tablero, nuevo_cerrado,nuevo_valor = realizar_movimiento(nodo.tablero, nueva_posicion,nodo.posicion, nodo.jugador,nodo.Cerrados)
        valor = nuevo_valor + (profundidad + 1)

        nuevo_nodo = Nodo(cambiar_turno(nodo.jugador),nuevo_tablero,valor,profundidad,Encontrar_Posicion(cambiar_turno(nodo.jugador),
                nuevo_tablero),Encontrar_Posicion(nodo.jugador,nuevo_tablero),nuevo_cerrado)
        nuevo_nodo.profundidad = profundidad + 1
        nodo.hijos.append(nuevo_nodo)
        generarArbol(nuevo_nodo,profundidadMax,profundidad + 1)

    return nodo


def MiniMax(nodo, profundidad, es_maximizando,alfa,beta):
    if profundidad == 0 or not nodo.hijos:
        return nodo.valor

    if es_maximizando:
        mejor_valor = float("-inf")
        for hijo in nodo.hijos:
            valor = MiniMax(hijo, profundidad - 1,False, alfa, beta)
            mejor_valor = max(mejor_valor, valor)
            alfa = max(alfa, mejor_valor)
            if beta <= alfa:
                break
        return mejor_valor
    else:
        peor_valor = float("inf")
        for hijo in nodo.hijos:
            valor = MiniMax(hijo, profundidad - 1, True,alfa, beta)
            peor_valor = min(peor_valor, valor)
            beta = min(beta, peor_valor)
            if beta <= alfa:
                break
        return peor_valor

def Mejor_movimiento(nodo,profundidad):
    mejor_valor = float("-inf")
    mejor_movimiento = None
    alfa = float("-inf")
    beta = float("inf")

    for hijo in nodo.hijos:
        valor = MiniMax(hijo, profundidad,False,alfa=alfa, beta=beta)  # Ajusta la profundidad según tus necesidades
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = hijo
        alfa = max(alfa, mejor_valor)

    return mejor_movimiento
    
def imprimir_arbol(nodo, nivel=0, desplazamiento=2, archivo=None):
    if archivo is None:
        # Si no se proporciona un archivo, imprimir en la consola
        archivo = sys.stdout

    if nodo is not None:
        # Agregar desplazamiento a la información de cada nodo
        desplazamiento_actual = desplazamiento * nivel

        print(" " * 2 * desplazamiento_actual + f"Jugador: {nodo.jugador}", file=archivo)
        if nodo.valor is not None:
            print(" " * 2 * desplazamiento_actual + f"Costo: {nodo.valor}", file=archivo)
        if nodo.profundidad is not None:
            print(" " * 2 * desplazamiento_actual + f"Profundidad: {nodo.profundidad}", file=archivo)
        if nodo.Cerrados is not None:
            print(" " * 2 * desplazamiento_actual + f"No_Accesibles: {nodo.Cerrados}", file=archivo)
        if nodo.posicion is not None:
            print(" " * 2 * desplazamiento_actual + f"Posición: {nodo.posicion}", file=archivo)
        if nodo.tablero is not None:
            print(" " * 2 * desplazamiento_actual + "Tablero:", file=archivo)
            for fila in nodo.tablero:
                print(" " * 2 * desplazamiento_actual + str(fila), file=archivo)
        print("-" * 40, file=archivo)
        for hijo in nodo.hijos:
            imprimir_arbol(hijo, nivel + 1, desplazamiento, archivo)



profundidad = 3
arbol = generarArbol(nodo_inicial,profundidad)
print("soijfoshofhsouehfohseofshefohseofhseofhs")
print(MiniMax(arbol,2,True,float("-inf"),float("inf")))
print("tablero: ")
print(Mejor_movimiento(arbol,profundidad).tablero)
print("profundidad: ",Mejor_movimiento(arbol,profundidad).profundidad)
print("Cerrados: ",Mejor_movimiento(arbol,profundidad).Cerrados)
print("costo: ",Mejor_movimiento(arbol,profundidad).valor)

print("oiahoghaoehgoahgaoiehgoaihegoahegoahega")
#imprimir_arbol(arbol)
with open('arbol.txt', 'w') as archivo:
    imprimir_arbol(arbol, archivo=archivo)
#print(MiniMax(arbol,True,float("-inf"),float("inf")))
#print("mejor movimiento")
#print(Mejor_movimiento(arbol).valor)
#print(Mejor_movimiento(arbol).tablero)

