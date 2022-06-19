import pygame
import Attitude.base as b

F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_GAUGE
F_COLOR_FG = b.COLOR_GAUGE_FG
F_COLOR_BG = b.COLOR_GAUGE_BG
C_KEY = b.COLOR_KEY

class Display (b.EFISElement):
	
	def __init__ (self):
		super().__init__((80, 40))
		self.buffer.set_colorkey (C_KEY)
		self.buffer.fill (C_KEY)
		self.text = pygame.font.Font (F_FILE, F_SIZE)
		# Frame with pointer
		r = self.buffer.get_rect()
		pygame.draw.polygon (self.buffer, F_COLOR_FG, [
			r.midright, (r.right-10, int(r.h/3)),
			(r.right-10, r.top), (r.left, r.top),
			(r.left, r.bottom-2), (r.right-10, r.bottom-2),
			(r.right-10, 2*int(r.h/3)), r.midright
		], 0)
		pygame.draw.polygon (self.buffer, F_COLOR_BG, [
			(r.right-3, r.centery), (r.right-13, int(r.h/3)),
			(r.right-13, 2*int(r.h/3)), (r.right-3, r.centery)
		], 0)
		r.size = (r.width - 14, r.height - 5)
		r.topleft = (2, 2)
		self.buffer.set_clip (r)
		self.buffer.fill (F_COLOR_BG)
		
	def set_value (self, value):
		fig = self.text.render (str(int(value)), True, F_COLOR_FG)
		r = fig.get_rect()
		r.right = self.rect.w - 18
		self.buffer.fill (F_COLOR_BG)
		self.buffer.blit (fig, r)
		
