import random

# Crear tablero de juego al azar
def init_game():
    '''
    Random board creation
    '''
    player1_pos = ()
    player2_pos = ()
    coin_pos = [(0, 0), (0, 1), (1, 0), (7, 0), (6, 0), (7, 1), (7, 7), (7, 6), (6, 7), (0, 7), (0, 6), (1, 7)]
    special_coins_pos = [(3, 3), (3, 4), (4, 3), (4, 4)]
    board = []

    def random_pos():
        while True:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if (x, y) not in coin_pos and (x, y) not in special_coins_pos and (x, y) != player1_pos:
                return (x, y)

    player1_pos = random_pos()
    player2_pos = random_pos()

    return player1_pos, player2_pos, coin_pos, special_coins_pos
