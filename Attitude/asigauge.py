import pygame
import base as b

FONT_SIZE = 40

FONT_COLOR = b.MKR_COLOR
FONT_BKGND = (40, 40, 40)
FRAME_COLOR = (200, 200, 200)

COLOR_KEY = (0, 0, 0)

class Display (b.EFISElement):
	
	def __init__ (self):
		super().__init__((100, 48))
		self.buffer.set_colorkey (COLOR_KEY)
		self.buffer.fill (COLOR_KEY)
		self.text = pygame.font.Font (b.FONT_FILE, FONT_SIZE)
		# Frame with pointer
		r = self.buffer.get_rect()
		pygame.draw.polygon (self.buffer, FRAME_COLOR, [
			r.midright, (r.right-10, int(r.h/3)),
			(r.right-10, r.top), (r.left, r.top),
			(r.left, r.bottom-2), (r.right-10, r.bottom-2),
			(r.right-10, 2*int(r.h/3)), r.midright
		], 0)
		pygame.draw.polygon (self.buffer, FONT_BKGND, [
			(r.right-3, r.centery), (r.right-13, int(r.h/3)),
			(r.right-13, 2*int(r.h/3)), (r.right-3, r.centery)
		], 0)
		r.size = (r.width - 14, r.height - 5)
		r.topleft = (2, 2)
		self.buffer.set_clip (r)
		self.buffer.fill (FONT_BKGND)
		
	def set_value (self, value):
		fig = self.text.render (str(int(value)), True, FONT_COLOR)
		r = fig.get_rect()
		r.right = self.rect.w - 18
		self.buffer.fill (FONT_BKGND)
		self.buffer.blit (fig, r)
		
