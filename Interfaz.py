import pygame as pyg, sys, os
import spritesheet

import chichenol
from button import Button
from dropdown import DropDown
from utils import *

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
P1_victory_path = os.path.join(main_path, 'Assets', "P1 victory.png")
P2_victory_path = os.path.join(main_path, 'Assets', "P2 victory.png")
results_path = os.path.join(main_path, "Assets", "Results.jpg")
tie_path = os.path.join(main_path, 'Assets', "Tie.png")
yoship_path = os.path.join(main_path, "Sprites", "yoship1.png")
yoshiIA_path = os.path.join(main_path, "Sprites", "yoship2.png")
icon_path = os.path.join(main_path, "Assets", "Yoshi_egg.png")
font_path = os.path.join(main_path, "Fonts", "wayoshi.ttf")
green_path = os.path.join(main_path, "Sprites", "Green Yoshi")
red_path = os.path.join(main_path, "Sprites", "Red Yoshi")
yellow_path = os.path.join(main_path, "Sprites", "Yellow Yoshi")
blue_path = os.path.join(main_path, "Sprites", "Blue Yoshi")
cyan_path = os.path.join(main_path, "Sprites", "Cyan Yoshi")
purple_path = os.path.join(main_path, "Sprites", "Purple Yoshi")
lavender_path = os.path.join(main_path, "Sprites", "Lavender Yoshi")
orange_path = os.path.join(main_path, "Sprites", "Orange Yoshi")
pink_path = os.path.join(main_path, "Sprites", "Pink Yoshi")
white_path = os.path.join(main_path, "Sprites", "White Yoshi")
black_path = os.path.join(main_path, "Sprites", "Black Yoshi")

# Sprite sheets paths

# Music and sound effects paths
main_theme = os.path.join(main_path, "Music", "main theme.mp3")
gameplay_theme = os.path.join(main_path, "Music", "gameplay.mp3")
credits_theme = os.path.join(main_path, "Music", "Credits.mp3")
egg_pop_path = os.path.join(main_path, "Music", "Egg pop.mp3")
P1_theme_path = os.path.join(main_path, "Music", "P1 Victory theme.mp3")
P1_loose_path = os.path.join(main_path, "Music", "P1 looses.mp3")
yoshi_jump_path = os.path.join(main_path, "Music", "yoshi jump.mp3")
yoshi_sound_path = os.path.join(main_path, "Music", "yoshi sound.mp3")

# Music and Sound initializers
pyg.mixer.music.load(main_theme)
pyg.mixer.music.play(-1)
pyg.mixer.music.set_volume(0.5)
egg_pop = pyg.mixer.Sound(egg_pop_path)
P1_loose = pyg.mixer.Sound(P1_loose_path)
yoshi_jump = pyg.mixer.Sound(yoshi_jump_path)
yoshi_sound = pyg.mixer.Sound(yoshi_sound_path)

# Background
background = pyg.image.load(background_path)
background_rect = background.get_rect()

credits_background = pyg.image.load(credits_bg_path)
credits_bg_rect = credits_background.get_rect()

results_background = pyg.image.load(results_path)
results_bg_rect = results_background.get_rect()

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

P1_victory = pyg.image.load(P1_victory_path)
P1_victory_rect = P1_victory.get_rect()
P2_victory = pyg.image.load(P2_victory_path)
P2_victory_rect = P2_victory.get_rect()
tie = pyg.image.load(tie_path)
tie_rect = tie.get_rect()

# FPS counter
clock = pyg.time.Clock()

# Buttons initializer
play_button = Button(egg_button, (170, 150), screen)
credits_button = Button(egg_button, (170, 400), screen)

#credits
text_list = [
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Trabajo Hecho por:",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Daniel Rosero (Tuki Dan)",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Geider Andres Montano (El yoshi negro)",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Deison Aleixer Cardona (Salsa-man)",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Mateo Duque (El verdadero Yoshi goddo)",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Guion de juego por:",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "El profe Oscar",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Heuristica:",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Daniel Rosero -La mente maestra-",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Geider Andres -El que le mete clean-",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Deison Aleixer -El que le dio cabeza un dia entero-",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Mateo Duque -El que nomas aseguro la compatibilidad con la UI-",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Diseno de interfaz:"
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Daniel Rosero -El que canta la musiquita-",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Geider Andres -El que le queria meter mano-",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Deison Aleixer -Con bendicion-",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Mateo Duque -El hombre interfaz-",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Con la colaboracion especial de:",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "Chsotoy -El que produce solo-"
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    "GRACIAS POR JUGAR!",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
    " ",
]

credits_font = pyg.font.Font(font_path, 30)
# create credits texts and their rects
text_objects = [credits_font.render(line, True, (0, 0, 0)) for line in text_list]
text_rects = [text_obj.get_rect(center=(WIDTH // 2, (i + 200) * (HEIGHT // (len(text_list) + 1)))) for i, text_obj
              in enumerate(text_objects)]


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
        self.victory = ''
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
        self.yoshi_color = 'green'
        self.ia_movement = (0, 0)
        self.player_movement = (0, 0)

        self.PLAYER1_POS, self.PLAYER2_POS, self.COIN_POS, self.SPECIAL_COINS_POS = init_game()

        # Animation variables:
        self.animation_cooldown = 120
        self.player_frame = 0
        self.ia_frame = 0
        self.player_last_update = pyg.time.get_ticks()
        self.ia_last_update = pyg.time.get_ticks()

        # Paths
        self.player_idle_path = os.path.join(red_path, 'idle.png')  # Player idle image
        self.ia_idle_path = os.path.join(green_path, 'idle.png')  # AI idle image
        self.player_move_path = os.path.join(red_path, 'move.png')
        self.ia_move_path = os.path.join(green_path, 'move.png')
        self.player_win_path = os.path.join(red_path, 'win.png')  # Player win image
        self.player_win = pyg.image.load(self.player_win_path)
        self.player_loose_path = os.path.join(red_path, 'loose.png')  # Player loose image
        self.player_loose = pyg.image.load(self.player_loose_path)
        self.ia_win_path = os.path.join(green_path, 'win.png')  # AI win image
        self.ia_win = pyg.image.load(self.ia_win_path)
        self.ia_loose_path = os.path.join(green_path, 'loose.png')  # AI loosing image
        self.ia_loose = pyg.image.load(self.ia_loose_path)
        self.player_card_path = os.path.join(red_path, 'card.png')  # Player card image
        self.player_card = pyg.image.load(self.player_card_path)
        self.ia_card_path = os.path.join(green_path, 'card.png')  # AI card image
        self.ia_card = pyg.image.load(self.ia_card_path)

        # Sprite Sheets
        self.player_sprite_load = pyg.image.load(self.player_idle_path)
        self.player_sprite = spritesheet.SpriteSheet(self.player_sprite_load)
        self.ia_sprite_load = pyg.image.load(self.ia_idle_path)
        self.ia_sprite = spritesheet.SpriteSheet(self.ia_sprite_load)
        self.player_move_sprite_load = pyg.image.load(self.player_move_path)
        self.player_move_sprite = spritesheet.SpriteSheet(self.player_move_sprite_load)
        self.ia_move_sprite_load = pyg.image.load(self.ia_move_path)
        self.ia_move_sprite = spritesheet.SpriteSheet(self.ia_move_sprite_load)
        self.player_move_load = pyg.image.load(self.player_move_path)
        self.ia_move_load = pyg.image.load(self.ia_move_path)


        # Animation lists
        self.player_idle_list = []
        self.ia_idle_list = []
        self.player_move_list = []
        self.ia_move_list = []

        self.animation_list_create(self.player_idle_list, 5, self.player_sprite)
        self.animation_list_create(self.ia_idle_list, 5, self.ia_sprite)
        self.animation_list_create(self.player_move_list, 17, self.player_move_sprite)
        self.animation_list_create(self.ia_move_list, 17, self.ia_move_sprite)

    def animation_list_create(self, list, steps, image):
        for i in range(steps):
            list.append(image.get_image(i, 75, 75, 1, (0, 0, 0)))


    def result(self):
        mouse_pos = pyg.mouse.get_pos()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            elif event.type == pyg.MOUSEMOTION:
                self.menu_button.is_hovered(mouse_pos, pyg.image.load(menu_button_path))

            if event.type == pyg.MOUSEBUTTONDOWN:
                if self.menu_button.collider(mouse_pos):
                    pyg.mixer.music.fadeout(2000)
                    self.state = 'menu'
                    play_music(main_theme, -1, 0.5)

        screen.blit(results_background, results_bg_rect)
        self.menu_button.draw()

        # Player 1 Card
        rect1 = pyg.Rect(20, 60, 300, 200)
        pyg.draw.rect(screen, (65, 60, 55), rect1, 0, 25, 25)

        draw_text(200, 115, "Player 1", "White", screen)  # Text

        # Player 2 Card
        rect2 = pyg.Rect(960, 60, 300, 200)
        pyg.draw.rect(screen, (65, 60, 55), rect2, 0, 25, 25)

        # Image
        draw_text(1140, 115, "Player 2", "White", screen)  # Text

        # Texts
        draw_text(115, 200, "Points:", "White", screen)
        draw_text(1065, 200, "Points:", "White", screen)

        # Scores
        draw_text(215, 200, str(self.PLAYER1_SCORE), "White", screen)
        draw_text(1165, 200, str(self.PLAYER2_SCORE), "White", screen)

        scaled_p1_text = pyg.transform.scale(P1_victory, (
            int(P1_victory_rect.width * self.scale_factor), int(P1_victory_rect.height * self.scale_factor)))
        scaled_p1_rect = scaled_p1_text.get_rect(topleft=(400, 50))
        if self.victory == 'P1':
            screen.blit(self.player_win, (40, 80))
            screen.blit(self.ia_loose, (980, 80))
            if self.scale_factor >= 1 or self.scale_factor <= 0.8:
                self.scale_speed = -self.scale_speed
            self.scale_factor += self.scale_speed

            screen.blit(scaled_p1_text, scaled_p1_rect)

        if self.victory == 'P2':
            screen.blit(self.ia_win, (980, 80))
            screen.blit(self.player_loose, (40, 80))
            scaled_p2_text = pyg.transform.scale(P2_victory, (
                int(P2_victory_rect.width * self.scale_factor), int(P2_victory_rect.height * self.scale_factor)))
            scaled_p2_rect = scaled_p2_text.get_rect(topleft=(400, 50))

            if self.scale_factor >= 1 or self.scale_factor <= 0.8:
                self.scale_speed = -self.scale_speed
            self.scale_factor += self.scale_speed

            screen.blit(scaled_p2_text, scaled_p2_rect)

        if self.victory == 'tie':
            screen.blit(self.player_card, (40, 80))
            screen.blit(self.ia_card, (980, 80))
            scaled_tie_text = pyg.transform.scale(tie, (
                int(tie_rect.width * self.scale_factor), int(tie_rect.height * self.scale_factor)))
            scaled_tie_rect = scaled_tie_text.get_rect(topleft=(500, 50))

            if self.scale_factor >= 1 or self.scale_factor <= 0.8:
                self.scale_speed = -self.scale_speed
            self.scale_factor += self.scale_speed

            screen.blit(scaled_tie_text, scaled_tie_rect)

        pyg.display.flip()



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
                    self.turn = 2
                    self.playing = False
                    self.depth = 0
                    self.victory = ''

                    # Graphics restart
                    self.ia_movement = (0, 0)
                    self.player_movement = (0, 0)
                    self.player_frame = 0
                    self.ia_frame = 0
                    self.player_last_update = pyg.time.get_ticks()
                    self.ia_last_update = pyg.time.get_ticks()

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
                return index

        for index, point in enumerate(special_coins):
            if point == move:
                self.is_special = True
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

                            else:
                                available = False
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
                    self.turn = 2
                    self.playing = False
                    self.depth = 0

                    # Graphics restart
                    self.ia_movement = (0, 0)
                    self.player_movement = (0, 0)
                    self.player_frame = 0
                    self.ia_frame = 0
                    # self.player_last_update = pyg.time.get_ticks()
                    # self.ia_last_update = pyg.time.get_ticks()

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

                if self.PLAYER1_POS[0] * CELL_WIDTH + 340 <= x <= self.PLAYER1_POS[0] * CELL_WIDTH + 340 + CELL_WIDTH \
                        and self.PLAYER1_POS[1] * CELL_HEIGHT + 60 <= y <= self.PLAYER1_POS[1] * CELL_HEIGHT + 60 + CELL_HEIGHT:
                    self.clicked = self.clicked ^ True

                # If the players clicks a green cell
                if self.clicked and self.turn == 1:
                    moves = self.available_moves(self.PLAYER1_POS, self.PLAYER2_POS, self.blocked_cells)
                    for move in moves:

                        if move != 0:
                            POS_I = move[0] * CELL_WIDTH + 340
                            POS_J = move[1] * CELL_HEIGHT + 60

                            if POS_I <= x <= POS_I + CELL_WIDTH and POS_J <= y <= POS_J + CELL_HEIGHT:
                                # Checks if the move gives points
                                index = self.check_moves(move, self.COIN_POS, self.SPECIAL_COINS_POS)

                                if index != None:
                                    if not self.is_special:
                                        self.PLAYER1_SCORE += 1
                                        self.blocked_cells.append(self.COIN_POS[index])
                                        self.COIN_POS[index] = 0
                                    elif self.is_special:
                                        self.PLAYER1_SCORE += 3
                                        self.blocked_cells.append(self.SPECIAL_COINS_POS[index])
                                        self.SPECIAL_COINS_POS[index] = 0

                                self.PLAYER1_POS = move
                                self.player_movement = move
                                self.clicked = False

                                self.turn = 4
                                self.player_frame = 0

                                break

        if self.turn == 2 and self.playing:
            self.PLAYER2_POS = chichenol.minimax(self.PLAYER2_POS, self.PLAYER1_POS, self.PLAYER2_SCORE,
                                                 self.PLAYER1_SCORE, self.COIN_POS, self.SPECIAL_COINS_POS,
                                                 self.blocked_cells, self.depth)
            self.ia_movement = chichenol.minimax(self.PLAYER2_POS, self.PLAYER1_POS, self.PLAYER2_SCORE,
                                                 self.PLAYER1_SCORE, self.COIN_POS, self.SPECIAL_COINS_POS,
                                                 self.blocked_cells, self.depth)

            index = self.check_moves(self.PLAYER2_POS, self.COIN_POS, self.SPECIAL_COINS_POS)
            if index != None:
                if not self.is_special:
                    self.PLAYER2_SCORE += 1
                    self.blocked_cells.append(self.COIN_POS[index])
                    self.COIN_POS[index] = 0
                elif self.is_special:
                    self.PLAYER2_SCORE += 3
                    self.blocked_cells.append(self.SPECIAL_COINS_POS[index])
                    self.SPECIAL_COINS_POS[index] = 0

            self.turn = 3
            self.ia_frame = 0

        # Animation variable
        player_current_time = pyg.time.get_ticks()
        ia_current_time = pyg.time.get_ticks()

        # Board and assets draw
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                POS_I = i * CELL_WIDTH
                POS_J = j * CELL_HEIGHT
                rect = pyg.Rect(POS_I + 340, POS_J + 60, CELL_WIDTH, CELL_HEIGHT)
                if (i + j) % 2 == 0:
                    pyg.draw.rect(screen, (240, 210, 185), rect)  # Draws the white square
                else:
                    pyg.draw.rect(screen, (65, 60, 55), rect)  # Draws the black square

                for pos in self.COIN_POS:
                    if (i, j) == pos:
                        screen.blit(coin, (POS_I + 340, POS_J + 60))

                for pos in self.SPECIAL_COINS_POS:
                    if (i, j) == pos:
                        screen.blit(special_coin, (POS_I + 340, POS_J + 60))

                for pos in self.blocked_cells:
                    if (i, j) == pos:
                        screen.blit(blocked_cell, (POS_I + 340, POS_J + 60))

                # Player graphic movement
                if self.turn == 4:
                    self.animation_cooldown = 120
                    if (i, j) == self.PLAYER1_POS:
                        if player_current_time - self.player_last_update >= self.animation_cooldown:
                            self.player_frame += 1
                            self.player_last_update = player_current_time

                            if self.player_frame == 3:
                                yoshi_jump.play()

                            if self.player_frame >= len(self.player_move_list):
                                self.player_frame = 0
                                self.animation_cooldown = 120
                                self.turn = 2
                        screen.blit(self.player_move_list[self.player_frame], (POS_I + 340, POS_J + 60))

                    if (i, j) == self.PLAYER2_POS:
                        if ia_current_time - self.ia_last_update >= self.animation_cooldown:
                            self.ia_frame += 1
                            self.ia_last_update = ia_current_time

                            if self.ia_frame >= len(self.ia_idle_list):
                                self.ia_frame = 0

                        screen.blit(self.ia_idle_list[self.ia_frame], (POS_I + 340, POS_J + 60))

                # AI graphic movement
                if self.turn == 3:
                    self.animation_cooldown = 120
                    if (i, j) == self.PLAYER2_POS:
                        if ia_current_time - self.ia_last_update >= self.animation_cooldown:
                            self.ia_frame += 1
                            self.ia_last_update = ia_current_time

                            if self.ia_frame == 3:
                                yoshi_jump.play()

                            if self.ia_frame >= len(self.ia_move_list):
                                self.ia_frame = 0
                                self.animation_cooldown = 120
                                self.turn = 1

                        screen.blit(self.ia_move_list[self.ia_frame], (POS_I + 340, POS_J + 60))


                    if (i, j) == self.PLAYER1_POS:
                        if player_current_time - self.player_last_update >= self.animation_cooldown:
                            self.player_frame += 1
                            self.player_last_update = player_current_time

                            if self.player_frame >= len(self.player_idle_list):
                                self.player_frame = 0

                        screen.blit(self.player_idle_list[self.player_frame], (POS_I + 340, POS_J + 60))

                # Update animation
                if self.turn == 2 or self.turn == 1:
                    if (i, j) == self.PLAYER1_POS:
                        if player_current_time - self.player_last_update >= self.animation_cooldown:
                            self.player_frame += 1
                            self.player_last_update = player_current_time

                            if self.player_frame >= len(self.player_idle_list):
                                self.player_frame = 0

                        screen.blit(self.player_idle_list[self.player_frame], (POS_I + 340, POS_J + 60))

                if self.turn == 2 or self.turn == 1:
                    if (i, j) == self.PLAYER2_POS:
                        if ia_current_time - self.ia_last_update >= self.animation_cooldown:
                            self.ia_frame += 1
                            self.ia_last_update = ia_current_time

                            if self.ia_frame >= len(self.ia_idle_list):
                                self.ia_frame = 0

                        screen.blit(self.ia_idle_list[self.ia_frame], (POS_I + 340, POS_J + 60))

                pyg.draw.rect(screen, (0, 0, 0), rect, 1)  # Draw the black lines


        # Player 1 card
        rect1 = pyg.Rect(20, 60, 300, 200)
        pyg.draw.rect(screen, (65, 60, 55), rect1, 0, 25, 25)
        # Image
        screen.blit(self.player_card, (40, 80))
        draw_text(200, 115, "Player 1", "White", screen)  # Texto

        # Player 2 card
        rect2 = pyg.Rect(960, 60, 300, 200)
        pyg.draw.rect(screen, (65, 60, 55), rect2, 0, 25, 25)
        # Image
        screen.blit(self.ia_card, (980, 80))
        draw_text(1140, 115, "Player 2", "White", screen)  # Texto

        # Texts
        draw_text(115, 200, "Points:", "White", screen)
        draw_text(80, 320, "Level:", "White", screen)
        draw_text(1065, 200, "Points:", "White", screen)

        # Scores
        draw_text(215, 200, str(self.PLAYER1_SCORE), "White", screen)
        draw_text(1165, 200, str(self.PLAYER2_SCORE), "White", screen)

        self.play_button.draw()
        self.restart_button.draw()
        self.menu_button.draw()

        self.dropdown.draw(screen)

        pyg.display.flip()

        if self.COIN_POS == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] and self.SPECIAL_COINS_POS == [0, 0, 0, 0]\
                and self.turn != 1 and self.turn != 2:
            self.turn = 5
            if self.PLAYER1_SCORE > self.PLAYER2_SCORE:
                pyg.mixer.music.fadeout(1000)
                play_music(P1_theme_path, 1, 0.5)
                self.victory = 'P1'
                self.state = 'results'

            elif self.PLAYER1_SCORE < self.PLAYER2_SCORE:
                P1_loose.play()
                self.victory = 'P2'
                self.state = 'results'
            else:
                self.victory = 'tie'
                self.state = 'results'

        pyg.display.flip()

    def credits(self):
        pyg.event.pump()
        font = pyg.font.Font(font_path, 50)
        speed = 1

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

        for i in range(len(text_list)):
            # Move text up
            text_rects[i].y -= (speed + 1)

            if text_rects[i].bottom < 360:
                # Text Vanishing
                alpha = text_objects[i].get_alpha()
                if alpha > 0:
                    text_objects[i].set_alpha(max(0, alpha - 3))

            # Verify if text line is completely out of the screen
            if text_rects[i].top <= 0:
                # Position reset
                text_rects[i].centerx = WIDTH // 2
                text_rects[i].centery = HEIGHT - 50
                # Transparency reset
                text_objects[i].set_alpha(255)

            screen.blit(credits_background, credits_bg_rect)

        for i in range(len(text_list)):
            screen.blit(text_objects[i], text_rects[i])

        screen.blit(scaled_logo, scaled_logo_rect)

        pyg.display.flip()

    def state_manager(self):
        if self.state == 'menu':
            self.menu()
        if self.state == 'play game':
            self.play_game()
        if self.state == 'credits':
            self.credits()
        if self.state == 'results':
            self.result()


game_state = GameState()
while True:
    game_state.state_manager()
    # FPS
    clock.tick(30)
