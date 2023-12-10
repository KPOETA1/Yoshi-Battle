import pygame as pyg
import os

pyg.init()
pyg.mixer.init()

# Paths
main_path = os.path.dirname(__file__)

# Music and sound effects paths
egg_pop_path = os.path.join(main_path, "Music", "Egg pop.mp3")

# Music and sound effects initializers
egg_pop = pyg.mixer.Sound(egg_pop_path)


class Button:

	def __init__(self, image, pos, screen):
		self.image = image
		self.normal_image = image
		self.screen = screen
		self.pos = pos
		self.rect = self.image.get_rect()
		self.rect.topleft = (pos[0], pos[1])
		self.sound_played = False

	def draw(self):
		self.screen.blit(self.image, (self.rect.x, self.rect.y))

	def update(self, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos[0], self.pos[1])

	def is_hovered(self, mouse_pos, image):
		is_hovered = self.rect.collidepoint(mouse_pos)
		if is_hovered:
			self.update(image)
			if not self.sound_played:
				egg_pop.play()
				self.sound_played = True

		else:
			self.update(self.normal_image)
			self.sound_played = False

	def collider(self, mouse_pos):
		return self.rect.collidepoint(mouse_pos)
