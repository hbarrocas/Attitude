from pathlib import Path
import pygame

# Module directory.
PATH_MODULE = Path(__file__).parent

# Constants
FONT_FILE = str(PATH_MODULE/'Jura-DemiBold.ttf')
FONT_SIZE_TAPE = 28
FONT_SIZE_GAUGE = 40

COLOR_BLACK = (0, 0, 0)
COLOR_DARKGREY = (40, 40, 40)
COLOR_GREEN = (0, 200, 0)
COLOR_YELLOW = (200, 200, 0)
COLOR_RED = (200, 0, 0)
COLOR_MAGENTA = (200, 40, 150)

COLOR_MARKER = (200, 200, 200)
COLOR_DISABLED = COLOR_RED
COLOR_TAPE_FG = COLOR_MARKER
COLOR_TAPE_BG = COLOR_BLACK
COLOR_GAUGE_FG = COLOR_MARKER
COLOR_GAUGE_BG = COLOR_DARKGREY
COLOR_SKY = (80, 100, 180)
COLOR_GND = (160, 90, 0)
COLOR_KEY = (0, 0, 0)


# Disabled red cross - gets drawn over an instrument when disabled
class Disabled:

	def __init__ (self, dim):
		self.buffer = pygame.Surface(dim)
		self.rect = self.buffer.get_rect()
		self.buffer.set_colorkey (COLOR_KEY)
		pygame.draw.rect (self.buffer, COLOR_DISABLED, self.rect, 8)
		pygame.draw.line (self.buffer, COLOR_DISABLED, self.rect.topleft, self.rect.bottomright, 8)
		pygame.draw.line (self.buffer, COLOR_DISABLED, self.rect.topright, self.rect.bottomleft, 8)

	def surface (self):
		return self.buffer
		
		
# Basic EFIS object. Can be nested to other EFISElements
class EFISElement:

	def __init__ (self, dim):
		self.buffer = pygame.Surface (dim)
		self.rect = self.buffer.get_rect()
		self._disabled = Disabled(dim)
		self.elements = []

	def disable (self):
		if self._disabled not in self.elements: self.elements.append (self._disabled)
	
	def enable (self):
		if self._disabled in self.elements: self.elements.remove (self._disabled)
				
	def surface (self):
		for e in self.elements:
			self.buffer.blit (e.surface(), e.rect)
		return self.buffer

