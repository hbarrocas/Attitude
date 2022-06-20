from pathlib import Path
import pygame, math

# Module directory.
PATH_MODULE = Path(__file__).parent

# Constants
FONT_FILE = str(PATH_MODULE/'Jura-DemiBold.ttf')
FONT_SIZE_TAPE = 24
FONT_SIZE_GAUGE = 32

COLOR_BLACK = (0, 0, 0)
COLOR_DARKGREY = (40, 40, 40)
COLOR_GREEN = (0, 200, 0)
COLOR_YELLOW = (200, 200, 0)
COLOR_RED = (200, 0, 0)
COLOR_MAGENTA = (200, 40, 150)
COLOR_CYAN = (60, 180, 250)

COLOR_MARKER = (200, 200, 200)
COLOR_DISABLED = COLOR_RED
COLOR_TAPE_FG = COLOR_MARKER
COLOR_TAPE_BG = COLOR_BLACK
COLOR_GAUGE_FG = COLOR_MARKER
COLOR_GAUGE_BG = COLOR_DARKGREY
COLOR_SKY = (30, 90, 180)
COLOR_GND = (160, 90, 0)
COLOR_KEY = (0, 0, 0)


class Area:

	def __init__ (self, sfc):
		self.buffer = sfc
		self.rect = sfc.get_rect()
		self.layers = []
	
	def render (self):
		for x in self.layers:
			self.buffer.blit (x.surface(), x.rect)


class Layer (Area):
	
	def __init__ (self, size):
		super().__init__(pygame.Surface(size))
		
	def surface (self):
		self.render()
		return self.buffer


class Disabled (Layer):
	
	def __init__ (self, size):
		super().__init__(size)
		self.buffer.set_colorkey (COLOR_KEY)
		pygame.draw.rect (self.buffer, COLOR_DISABLED, self.rect, 8)
		pygame.draw.line (self.buffer, COLOR_DISABLED, self.rect.topleft, self.rect.bottomright, 8)
		pygame.draw.line (self.buffer, COLOR_DISABLED, self.rect.topright, self.rect.bottomleft, 8)


class Widget (Area):

	def __init__ (self, sfc, rect):
		super().__init__ (sfc.subsurface(rect))
		self._disabled = Disabled (rect.size)
		
	def disable (self):
		if self._disabled not in self.layers:
			self.layers.append (self._disabled)

	def enable (self):
		if self._disabled in self.layers:
			self.layers.remove (self._disabled)


# Utility functions
def radial (centre, radius, angle):
	return (centre[0]+radius*math.cos(angle), centre[1]-radius*math.sin(angle))
