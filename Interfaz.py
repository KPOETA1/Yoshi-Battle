import pygame as pyg, sys, os

import chichenol
from button import Button
from dropdown import DropDown
from utils import *
from chichenol import minimax

# Initializers
pyg.init()
pyg.mixer.init()
state = 'menu'

# Screen
WIDTH, HEIGHT = 1280, 720
screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Yoshi's Battle")
BOARD_SIZE = 8
knight_N=2
CELL_WIDTH = 75
CELL_HEIGHT = 75

# Paths
main_path = os.path.dirname(__file__)
logo_path = os.path.join(main_path, "Assets", "Yoshi's Battle logo.png")
background_path = os.path.join(main_path, "Assets", "Yoshi's Battle background.jpg")
credits_bg_path = os.path.join(main_path, "Assets", "credits background.jpg")
egg_button_path = os.path.join(main_path, "Assets", "Yoshi_Egg.png")
play_button_path = os.path.join(main_path, "Assets", "Yoshi_Egg_play.png")
credits_button_path = os.path.join(main_path, "Assets", "Yoshi_Egg_credits.png")
restart_button_path = os.path.join(main_path, "Assets", "Yoshi_Egg_restart.png")
menu_button_path = os.path.join(main_path, "Assets", "Yoshi_Egg_menu.png")
coin_path = os.path.join(main_path, "Assets", "coin.png")
special_coin_path = os.path.join(main_path, "Assets", "flower.png")
blocked_cell_path = os.path.join(main_path, "Assets", "piranha.png")
yoship_path = os.path.join(main_path, "Sprites", "yoship1.png")
yoshiIA_path = os.path.join(main_path, "Sprites", "yoship2.png")
icon_path = os.path.join(main_path, "Assets", "Yoshi_egg.png")
font_path = os.path.join(main_path, "Fonts", "wayoshi.ttf")

# Music and sound effects paths
main_theme = os.path.join(main_path, "Music", "main theme.mp3")
gameplay_theme = os.path.join(main_path, "Music", "gameplay.mp3")
credits_theme = os.path.join(main_path, "Music", "Credits.mp3")
egg_pop_path = os.path.join(main_path, "Music", "Egg pop.mp3")

# Music and Sound initializers
pyg.mixer.music.load(main_theme)
pyg.mixer.music.play(-1)
pyg.mixer.music.set_volume(0.5)
egg_pop = pyg.mixer.Sound(egg_pop_path)

# Background
background = pyg.image.load(background_path)
background_rect = background.get_rect()

credits_background = pyg.image.load(credits_bg_path)
credits_bg_rect = credits_background.get_rect()

# Image Load
logo = pyg.image.load(logo_path)
logo_rect = logo.get_rect()

icon = pyg.image.load(icon_path)
pyg.display.set_icon(icon)

egg_button = pyg.image.load(egg_button_path)

yoship = pyg.image.load(yoship_path)
yoshiIA = pyg.image.load(yoshiIA_path)
blocked_cell = pyg.image.load(blocked_cell_path)

coin = pyg.image.load(coin_path)
special_coin = pyg.image.load(special_coin_path)

# FPS counter
clock = pyg.time.Clock()

# Buttons initializer
play_button = Button(egg_button, (170, 150), screen)
credits_button = Button(egg_button, (170, 400), screen)


def play_music(music_path, play_count, volume):  # Music player
    pyg.mixer.music.load(music_path)
    pyg.mixer.music.play(play_count)
    pyg.mixer.music.set_volume(volume)


def draw_text(x, y, string, col, window):
    font = pyg.font.Font(font_path, 30)
    text = font.render(string, True, col)
    textbox = text.get_rect(center=(x,y))
    window.blit(text, textbox)


class GameState:
    def __init__(self):
        self.state = 'menu'
        self.scale_factor = 1.0
        self.scale_speed = 0.01
        self.turn = 1
        self.clicked = False
        self.playing = False
        self.is_special = False
        self.depth = 0
        self.dropdown = DropDown(
         [(85, 85, 85), (149, 149, 149)],
         [(85, 85, 85), (149, 149, 149)],
         150, 300, 170, 50,
         pyg.font.Font(font_path, 30),
         "Select level", ["Beginner", "Amateur", "Expert"])
        self.PLAYER1_SCORE = 0
        self.PLAYER2_SCORE = 0
        self.blocked_cells = []
        self.play_button = Button(egg_button, (10, 500), screen)
        self.restart_button = Button(egg_button, (170, 500), screen)
        self.menu_button = Button(egg_button, (1050, 400), screen)
        self.yoship_rect = yoship.get_rect()
        self.yoshiIA_rect = yoshiIA.get_rect()

        self.PLAYER1_POS, self.PLAYER2_POS, self.COIN_POS, self.SPECIAL_COINS_POS = init_game()

    def menu(self):
        mouse_pos = pyg.mouse.get_pos()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            elif event.type == pyg.MOUSEMOTION:
                mouse_pos = pyg.mouse.get_pos()
                play_button.is_hovered(mouse_pos, pyg.image.load(play_button_path))
                credits_button.is_hovered(mouse_pos, pyg.image.load(credits_button_path))
            if event.type == pyg.MOUSEBUTTONDOWN:
                if play_button.collider(mouse_pos):
                    self.PLAYER1_POS, self.PLAYER2_POS, self.COIN_POS, self.SPECIAL_COINS_POS = init_game()
                    self.PLAYER1_SCORE = 0
                    self.PLAYER2_SCORE = 0
                    self.blocked_cells = []
                    self.clicked = False
                    self.turn = 1
                    self.playing = False
                    self.depth = 0
                    pyg.mixer.music.fadeout(2000)
                    self.state = 'play game'
                    play_music(gameplay_theme, -1, 0.5)

                if credits_button.collider(mouse_pos):
                    pyg.mixer.music.fadeout(2000)
                    self.state = 'credits'
                    play_music(credits_theme, 1, 0.5)

        scaled_logo = pyg.transform.scale(logo, (
            int(logo_rect.width * self.scale_factor), int(logo_rect.height * self.scale_factor)))
        scaled_logo_rect = scaled_logo.get_rect(center=logo_rect.center)

        if self.scale_factor >= 1 or self.scale_factor <= 0.8:
            self.scale_speed = -self.scale_speed
        self.scale_factor += self.scale_speed

        # Screen elements draw
        screen.blit(background, background_rect)
        screen.blit(scaled_logo, scaled_logo_rect)
        play_button.draw()
        credits_button.draw()

        # Screen update
        pyg.display.flip()

    def check_moves(self, move, coins, special_coins):
        for index, point in enumerate(coins):
            if point == move:
                self.is_special = False
                print('chequea no especial', self.is_special)
                return index

        for index, point in enumerate(special_coins):
            if point == move:
                self.is_special = True
                print('chequea especial', self.is_special)
                return index

        return None

    def available_moves(self, position, positionIA, position_blocked):
        moves = []
        x = position[0]
        y = position[1]
        available = False

        if x - 1 >= 0 and x - 1 <= 7:
            if y - 2 >= 0 and y - 2 <= 7:
                if positionIA != (x - 1, y - 2):
                    if not position_blocked:
                        available = True
                    else:
                        for pos in position_blocked:
                            if pos != (x - 1, y - 2):
                                available = True
                                print(available)

                            else:
                                available = False
                                print(available)
                                break

                    if available:
                        moves.append((x - 1, y - 2))

            if y + 2 >= 0 and y + 2 <= 7:
                if positionIA != (x - 1, y + 2):
                    if not position_blocked:
                        available = True
                    else:
                        for pos in position_blocked:
                            if pos != (x - 1, y + 2):
                                available = True
                            else:
                                available = False
                                break

                    if available:
                        moves.append((x - 1, y + 2))

        if x + 1 >= 0 and x + 1 <= 7:
            if y - 2 >= 0 and y - 2 <= 7:
                if positionIA != (x + 1, y - 2):
                    if not position_blocked:
                        available = True
                    else:
                        for pos in position_blocked:
                            if pos != (x + 1, y - 2):
                                available = True
                            else:
                                available = False
                                break

                    if available:
                        moves.append((x + 1, y - 2))

            if y + 2 >= 0 and y + 2 <= 7:
                if positionIA != (x + 1, y + 2):
                    if not position_blocked:
                        available = True
                    else:
                        for pos in position_blocked:
                            if pos != (x + 1, y + 2):
                                available = True
                            else:
                                available = False
                                break

                    if available:
                        moves.append((x + 1, y + 2))

        if x - 2 >= 0 and x - 2 <= 7:
            if y - 1 >= 0 and y - 1 <= 7:
                if positionIA != (x - 2, y - 1):
                    if not position_blocked:
                        available = True
                    else:
                        for pos in position_blocked:
                            if pos != (x - 2, y - 1):
                                available = True
                            else:
                                available = False
                                break

                    if available:
                        moves.append((x - 2, y - 1))

            if y + 1 >= 0 and y + 1 <= 7:
                if positionIA != (x - 2, y + 1):
                    if not position_blocked:
                        available = True
                    else:
                        for pos in position_blocked:
                            if pos != (x - 2, y + 1):
                                available = True
                            else:
                                available = False

                    if available:
                        moves.append((x - 2, y + 1))

        if x + 2 >= 0 and x + 2 <= 7:
            if y - 1 >= 0 and y - 1 <= 7:
                if positionIA != (x + 2, y - 1):
                    if not position_blocked:
                        available = True
                    else:
                        for pos in position_blocked:
                            if pos != (x + 2, y - 1):
                                available = True
                            else:
                                available = False
                                break

                    if available:
                        moves.append((x + 2, y - 1))

            if y + 1 >= 0 and y + 1 <= 7:
                if positionIA != (x + 2, y + 1):
                    if not position_blocked:
                        available = True
                    else:
                        for pos in position_blocked:
                            if pos != (x + 2, y + 1):
                                available = True
                            else:
                                available = False
                                break

                    if available:
                        moves.append((x + 2, y + 1))

        print('lista de posibles movimientos ', moves)

        return moves

    def play_game(self):
        x, y = pyg.mouse.get_pos()
        mouse_pos = pyg.mouse.get_pos()
        pyg.event.pump()
        screen.blit(background, background_rect)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            elif event.type == pyg.MOUSEMOTION:
                mouse_pos = pyg.mouse.get_pos()
                self.play_button.is_hovered(mouse_pos, pyg.image.load(play_button_path))
                self.restart_button.is_hovered(mouse_pos, pyg.image.load(restart_button_path))
                self.menu_button.is_hovered(mouse_pos, pyg.image.load(menu_button_path))

            selected_alg = self.dropdown.update(event)
            if selected_alg >= 0:
                self.dropdown.main = self.dropdown.options[selected_alg]

            if event.type == pyg.MOUSEBUTTONDOWN:
                mouse_pos = pyg.mouse.get_pos()
                if self.menu_button.collider(mouse_pos):
                    pyg.mixer.music.fadeout(2000)
                    self.state = 'menu'
                    play_music(main_theme, -1, 0.5)
                if self.restart_button.collider(mouse_pos):
                    self.PLAYER1_POS, self.PLAYER2_POS, self.COIN_POS, self.SPECIAL_COINS_POS = init_game()
                    self.PLAYER1_SCORE = 0
                    self.PLAYER2_SCORE = 0
                    self.blocked_cells = []
                    self.clicked = False
                    self.turn = 1
                    self.playing = False
                    self.depth = 0
                if self.play_button.collider(mouse_pos):
                    if self.dropdown.main == "Beginner" :
                        print("Beginner")
                        self.depth = 2
                        self.playing = True

                    if self.dropdown.main == "Amateur" :
                        print("Amateur")
                        self.depth = 4
                        self.playing = True

                    if self.dropdown.main == "Expert" :
                        print("Expert")
                        self.depth = 6
                        self.playing = True

                if self.PLAYER1_POS[0] * CELL_WIDTH + 340 <= x <= self.PLAYER1_POS[0] * CELL_WIDTH + 340 + CELL_WIDTH and \
                        self.PLAYER1_POS[1] * CELL_HEIGHT + 60 <= y <= self.PLAYER1_POS[1] * CELL_HEIGHT + 60 + CELL_HEIGHT:
                    self.clicked = self.clicked ^ True
                    print('el clic: ', self.clicked)

                # If the players clicks a green cell
                if self.clicked and self.turn == 1:
                    moves = self.available_moves(self.PLAYER1_POS, self.PLAYER2_POS, self.blocked_cells)
                    for move in moves:

                        if move != 0:
                            POS_I = move[0] * CELL_WIDTH + 340
                            POS_J = move[1] * CELL_HEIGHT + 60
                            print('posiciones en el tablero ', POS_I, POS_J)
                            print('movimiento actual ', move)

                            if POS_I <= x <= POS_I + CELL_WIDTH and POS_J <= y <= POS_J + CELL_HEIGHT:
                                print('No se que es esta monda')
                                # Checks if the move gives points
                                index = self.check_moves(move, self.COIN_POS, self.SPECIAL_COINS_POS)

                                if index != None:
                                    if not self.is_special:
                                        self.PLAYER1_SCORE += 1
                                        self.blocked_cells.append(self.COIN_POS[index])
                                        self.COIN_POS[index] = 0
                                        print('No es especial', self.is_special)
                                        print(self.blocked_cells)
                                    elif self.is_special:
                                        print('es especial', self.is_special)
                                        self.PLAYER1_SCORE += 3
                                        self.blocked_cells.append(self.SPECIAL_COINS_POS[index])
                                        self.SPECIAL_COINS_POS[index] = 0

                                self.PLAYER1_POS = move
                                print(move)
                                print(POS_I, POS_J)
                                self.clicked = False

                                self.turn = 2

                                break

        if self.turn == 2 and self.playing:
            self.PLAYER2_POS = chichenol.minimax(self.PLAYER2_POS, self.PLAYER1_POS, self.PLAYER2_SCORE,
                                                 self.PLAYER1_SCORE, self.COIN_POS, self.SPECIAL_COINS_POS,
                                                 self.blocked_cells, self.depth)
            # print(PLAYER1_POS)
            # print(PLAYER2_POS)
            # print(BOARD)
            index = self.check_moves(self.PLAYER2_POS, self.COIN_POS, self.SPECIAL_COINS_POS)
            # print(self.PLAYER2_POS)
            if index != None:
                if not self.is_special:
                    self.PLAYER2_SCORE += 1
                    self.blocked_cells.append(self.COIN_POS[index])
                    self.COIN_POS[index] = 0
                elif self.is_special:
                    self.PLAYER2_SCORE += 3
                    self.blocked_cells.append(self.SPECIAL_COINS_POS[index])
                    self.SPECIAL_COINS_POS[index] = 0

            self.turn = 1

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                POS_I = i * CELL_WIDTH
                POS_J = j * CELL_HEIGHT
                rect = pyg.Rect(POS_I + 340, POS_J + 60, CELL_WIDTH, CELL_HEIGHT)
                if (i + j) % 2 == 0:
                    pyg.draw.rect(screen, (240, 210, 185), rect)  # Dibuja el cuadro blanco
                else:
                    pyg.draw.rect(screen, (65, 60, 55), rect)  # Dibuja el cuadro negro

                for pos in self.COIN_POS:
                    if (i, j) == pos:
                        screen.blit(coin, (POS_I + 340, POS_J + 60))

                for pos in self.SPECIAL_COINS_POS:
                    if (i, j) == pos:
                        screen.blit(special_coin, (POS_I + 340, POS_J + 60))

                for pos in self.blocked_cells:
                    if (i, j) == pos:
                        screen.blit(blocked_cell, (POS_I + 340, POS_J + 60))

                if (i, j) == self.PLAYER1_POS:
                    screen.blit(yoship, (POS_I + 345, POS_J + 65))
                elif (i, j) == self.PLAYER2_POS:
                    screen.blit(yoshiIA, (POS_I + 345, POS_J + 65))

                pyg.draw.rect(screen, (0, 0, 0), rect, 1)  # Dibuja el borde negro


        # Tarjeta del jugador 1
        rect1 = pyg.Rect(20, 60, 300, 200)
        pyg.draw.rect(screen, (65, 60, 55), rect1, 0, 25, 25)
        # Imagen
        screen.blit(yoship, (40, 80))
        draw_text(200, 115, "Player 1", "White", screen)  # Texto

        # Tarjeta del jugador 2
        rect2 = pyg.Rect(960, 60, 300, 200)
        pyg.draw.rect(screen, (65, 60, 55), rect2, 0, 25, 25)
        # Imagen
        screen.blit(yoshiIA, (980, 80))
        draw_text(1140, 115, "Player 2", "White", screen)  # Texto

        # Textos
        draw_text(115, 200, "Points:", "White", screen)
        draw_text(80, 320, "Level:", "White", screen)
        draw_text(1065, 200, "Points:", "White", screen)

        # Puntajes
        draw_text(215, 200, str(self.PLAYER1_SCORE), "White", screen)
        draw_text(1165, 200, str(self.PLAYER2_SCORE), "White", screen)

        self.play_button.draw()
        self.restart_button.draw()
        self.menu_button.draw()

        self.dropdown.draw(screen)

        if self.COIN_POS == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] and self.SPECIAL_COINS_POS == [0, 0, 0, 0]\
                and self.turn != 1 and self.turn != 2:
            self.turn = 5
            if self.PLAYER1_SCORE > self.PLAYER2_SCORE:
                BOARD_TEXT = "Player 1 wins!"
            elif self.PLAYER1_SCORE < self.PLAYER2_SCORE:
                BOARD_TEXT = "Player 2 wins!"
            else:
                BOARD_TEXT = "It's a tie!"

        pyg.display.flip()

    def credits(self):
        pyg.event.pump()
        font = pyg.font.Font(font_path, 50)

        lines = [
            "primera linea",
            "Segunda lineaaa",
            "Tercera lineaaa",
            "Cuarta lineaaa",
            "Quinta lineaaaaa"
        ]



        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            if event.type == pyg.MOUSEBUTTONDOWN:
                pyg.mixer.music.fadeout(2000)
                self.state = 'menu'
                play_music(main_theme, -1, 0.5)

        scaled_logo = pyg.transform.scale(logo, (
            int(logo_rect.width * self.scale_factor), int(logo_rect.height * self.scale_factor)))
        scaled_logo_rect = scaled_logo.get_rect(center=(WIDTH // 2, 70))

        if self.scale_factor >= 1 or self.scale_factor <= 0.8:
            self.scale_speed = -self.scale_speed
        self.scale_factor += self.scale_speed

        screen.blit(credits_background, credits_bg_rect)
        screen.blit(scaled_logo, scaled_logo_rect)
        text_objects = [
            (font.render(line, True, (0, 255, 0)), (WIDTH // 2 - font.size(line)[0] // 2, HEIGHT + idx * 40))
            for idx, line in enumerate(lines)]

        for idx, (text, pos) in enumerate(text_objects):
            pos = (pos[0], pos[1] - 2)

            if pos[1] + text.get_height() < 0:
                text_objects[idx] = (text, WIDTH // 2 - text.get_width() // 2, HEIGHT + (len(lines) - 1) * 40)
            else:
                screen.blit(text, pos)

        pyg.display.flip()

    def state_manager(self):
        if self.state == 'menu':
            self.menu()
        if self.state == 'play game':
            self.play_game()
        if self.state == 'credits':
            self.credits()


game_state = GameState()
while True:
    game_state.state_manager()
    # FPS
    clock.tick(30)