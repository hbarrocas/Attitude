import pygame
import base as b

DISP_FONT_SIZE = 40
ROLL_FONT_SIZE = 30
FONT_COLOR = b.MKR_COLOR
FONT_BKGND = (40, 40, 40)
FRAME_COLOR = (200, 200, 200)

COLOR_KEY = (0, 0, 0)

class DisplayRoller (b.EFISElement):

	def __init__ (self):
		super().__init__((40, ROLL_FONT_SIZE * 6))
		self.buffer.fill (FONT_BKGND, self.rect)
		self.text = pygame.font.Font (b.FONT_FILE, ROLL_FONT_SIZE)
		num_y = range (0, ROLL_FONT_SIZE*6, ROLL_FONT_SIZE)
		for n in range(6):
			fig = self.text.render ("{0:0>2}".format((n % 5)*20), True, FONT_COLOR)
			r = fig.get_rect()
			r.top = num_y[n]
			self.buffer.blit (fig, r)

	def set_value (self, value):
		offset = (value % 100) / 20
		self.rect.top = (-offset if value > 0 else -5+offset) * ROLL_FONT_SIZE + 4


class Display (b.EFISElement):
	
	def __init__ (self):
		super().__init__((130, 48))
		self.buffer.set_colorkey(COLOR_KEY)
		self.buffer.fill (COLOR_KEY)
		self.text = pygame.font.Font (b.FONT_FILE, DISP_FONT_SIZE)

		# Frame shape
		r = self.buffer.get_rect()
		pygame.draw.polygon (self.buffer, FRAME_COLOR, [
			r.midleft, (r.left+10, int(r.h/3)),
			(r.left+10, r.top), (r.right-2, r.top),
			(r.right-2, r.bottom-2), (r.left+10, r.bottom-2),
			(r.left+10, 2*int(r.h/3)), r.midleft
		], 0)
		pygame.draw.polygon (self.buffer, FONT_BKGND, [
			(r.left+3, r.centery), (r.left+13, int(r.h/3)),
			(r.left+13, 2*int(r.h/3)), (r.left+3, r.centery)
		], 0)
		r.size = (r.width - 14, r.height - 5)
		r.topleft = (12, 2)
		
		# Flight Level display (hundred feet units)
		self.FLdisp = self.buffer.subsurface (r)
		self.FLdisp.fill (FONT_BKGND)

		# Rolling numbers' window (20 feet units)
		w = pygame.Rect ((self.rect.right-40, self.rect.top+6), (38, 30))
		self.buffer.set_clip (w)
		self.roller = DisplayRoller ()
		self.roller.rect.right = self.rect.w
		self.elements.append (self.roller)
	
	def set_value (self, value):
		self.roller.set_value (value)
		self.FLdisp.fill (FONT_BKGND)
		fig = self.text.render (str(int(value/100)), True, FONT_COLOR)
		r = fig.get_rect()
		r.right = self.rect.right-40-12		
		self.FLdisp.blit (fig, r)
		
