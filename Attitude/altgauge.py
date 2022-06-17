import pygame
import Attitude.base as b

F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_GAUGE
R_SIZE = int(b.FONT_SIZE_GAUGE*3/4)
F_COLOR_FG = b.COLOR_GAUGE_FG
F_COLOR_BG = b.COLOR_GAUGE_BG
C_KEY = b.COLOR_KEY

class DisplayRoller (b.EFISElement):

	def __init__ (self):
		super().__init__((40, R_SIZE * 6))
		self.buffer.fill (F_COLOR_BG, self.rect)
		self.text = pygame.font.Font (F_FILE, R_SIZE)
		num_y = range (0, R_SIZE*6, R_SIZE)
		for n in range(6):
			fig = self.text.render ("{0:0>2}".format((n % 5)*20), True, F_COLOR_FG)
			r = fig.get_rect()
			r.top = num_y[n]
			self.buffer.blit (fig, r)

	def set_value (self, value):
		offset = (value % 100) / 20
		self.rect.top = (-offset if value > 0 else -5+offset) * R_SIZE + 4


class Display (b.EFISElement):
	
	def __init__ (self):
		super().__init__((130, 48))
		self.buffer.set_colorkey(C_KEY)
		self.buffer.fill (C_KEY)
		self.text = pygame.font.Font (F_FILE, F_SIZE)

		# Frame shape
		r = self.buffer.get_rect()
		pygame.draw.polygon (self.buffer, F_COLOR_FG, [
			r.midleft, (r.left+10, int(r.h/3)),
			(r.left+10, r.top), (r.right-2, r.top),
			(r.right-2, r.bottom-2), (r.left+10, r.bottom-2),
			(r.left+10, 2*int(r.h/3)), r.midleft
		], 0)
		pygame.draw.polygon (self.buffer, F_COLOR_BG, [
			(r.left+3, r.centery), (r.left+13, int(r.h/3)),
			(r.left+13, 2*int(r.h/3)), (r.left+3, r.centery)
		], 0)
		r.size = (r.width - 14, r.height - 5)
		r.topleft = (12, 2)
		
		# Flight Level display (hundred feet units)
		self.FLdisp = self.buffer.subsurface (r)
		self.FLdisp.fill (F_COLOR_BG)

		# Rolling numbers' window (20 feet units)
		w = pygame.Rect ((self.rect.right-40, self.rect.top+6), (38, 30))
		self.buffer.set_clip (w)
		self.roller = DisplayRoller ()
		self.roller.rect.right = self.rect.w
		self.elements.append (self.roller)
	
	def set_value (self, value):
		self.roller.set_value (value)
		self.FLdisp.fill (F_COLOR_BG)
		fig = self.text.render (str(int(value/100)), True, F_COLOR_FG)
		r = fig.get_rect()
		r.right = self.rect.right-40-12		
		self.FLdisp.blit (fig, r)
		
