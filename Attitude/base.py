from pathlib import Path
import pygame

# Module directory. Font file resides here
MODULE_PATH = Path(__file__).parent

# Constants used on all modules
#FONT_FILE = MODULE_PATH / 'Jura-DemiBold.ttf'
FONT_FILE = 'Jura-DemiBold.ttf'
EFIS_SIZE = (800, 800)
MKR_COLOR = (200, 200, 200)
SKY_COLOR = (80, 100, 180)
GND_COLOR = (160, 90, 0)

DISABLED_COLOR = (200, 0, 0)

COLOR_KEY = (0, 0, 0)

# Disabled red cross - gets drawn over an instrument when disabled
class Disabled:

	def __init__ (self, dim):
		self.buffer = pygame.Surface(dim)
		self.rect = self.buffer.get_rect()
		self.buffer.set_colorkey (COLOR_KEY)
		pygame.draw.rect (self.buffer, DISABLED_COLOR, self.rect, 8)
		pygame.draw.line (self.buffer, DISABLED_COLOR, self.rect.topleft, self.rect.bottomright, 8)
		pygame.draw.line (self.buffer, DISABLED_COLOR, self.rect.topright, self.rect.bottomleft, 8)

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

