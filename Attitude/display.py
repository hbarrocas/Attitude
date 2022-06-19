import pygame
import Attitude.base as b

F_FILE = b.FONT_FILE
F_SIZE_VAL = b.FONT_SIZE_GAUGE
F_SIZE_TITLE = 25
F_COLOR_VAL_FG = b.COLOR_MAGENTA
F_COLOR_TITLE_FG = b.COLOR_MARKER
F_COLOR_BG = b.COLOR_TAPE_BG
C_KEY = b.COLOR_KEY

class Baro (b.EFISElement):
	
	def __init__ (self):
		super().__init__((130, 42))
		self.text_title = pygame.font.Font (F_FILE, F_SIZE_TITLE)
		self.text_val = pygame.font.Font (F_FILE, F_SIZE_VAL)
		self.buffer.fill (F_COLOR_BG)
		ttl = self.text_title.render ("hPa", True, F_COLOR_TITLE_FG)
		r = ttl.get_rect()
		r.midleft = self.rect.midleft
		self.buffer.blit (ttl, r)
		self.buffer.set_clip (pygame.Rect((r.right+5, 0), (self.rect.w-r.right-5, self.rect.h)))
		
	def set_value (self, value):
		fig = self.text_val.render (str(int(value)), True, b.COLOR_CYAN)
		r = fig.get_rect()
		r.bottomright = self.buffer.get_rect().bottomright
		self.buffer.fill (F_COLOR_BG)
		self.buffer.blit (fig, r)

		
class GSpeed (b.EFISElement):
	
	def __init__ (self):
		super().__init__((90, 42))
		self.text_title = pygame.font.Font (F_FILE, F_SIZE_TITLE)
		self.text_val = pygame.font.Font (F_FILE, F_SIZE_VAL)
		self.buffer.fill (F_COLOR_BG)
		ttl = self.text_title.render ("GS", True, F_COLOR_TITLE_FG)
		r = ttl.get_rect()
		r.midleft = self.rect.midleft
		self.buffer.blit (ttl, r)
		self.buffer.set_clip (pygame.Rect((r.right+5, 0), (self.rect.w-r.right-5, self.rect.h)))
		
	def set_value (self, value):
		fig = self.text_val.render (str(int(value)), True, b.COLOR_MAGENTA)
		r = fig.get_rect()
		r.bottomright = self.buffer.get_rect().bottomright
		self.buffer.fill (F_COLOR_BG)
		self.buffer.blit (fig, r)
		
