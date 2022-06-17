import pygame
import Attitude.base as b

C_KEY = b.COLOR_KEY
# Indicator bar colour
I_COLOR = b.COLOR_MAGENTA
# Font
F_COLOR = b.COLOR_TAPE_FG
F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_TAPE
# Markers
M_COLOR = b.COLOR_MARKER
M_SHORT = 12
M_LONG = 25
M_COUNT = 4
M_CENTRE = 2


class Scale (b.EFISElement):

	def __init__ (self, dim):
		super().__init__(dim)
		self.buffer.set_colorkey(C_KEY)
		self.M_SPACING = int((self.rect.h - 50)/M_COUNT)
		self.text = pygame.font.Font (F_FILE, F_SIZE)
		pygame.draw.line (self.buffer, M_COLOR, (self.rect.w-2, 25), (self.rect.w-2, self.rect.h-25), 2)
		m_yl = range (25, self.rect.h, self.M_SPACING)
		m_ys = range (25+int(self.M_SPACING/2), self.rect.h, self.M_SPACING)
		for n in range(M_COUNT+1):
			pygame.draw.line (self.buffer, M_COLOR, (self.rect.w, m_yl[n]), (self.rect.w-M_LONG, m_yl[n]), 2)
			fig = self.text.render (str(M_CENTRE-n), True, F_COLOR)
			r = fig.get_rect()
			r.midright = (self.rect.w - M_LONG - 5, m_yl[n])
			self.buffer.blit(fig, r)
		for n in range (M_COUNT):
			pygame.draw.line (self.buffer, M_COLOR, (self.rect.w, m_ys[n]), (self.rect.w-M_SHORT, m_ys[n]), 2)
		
		
class VSI (b.EFISElement):
	
	def __init__ (self):
		super().__init__((50, 450))
		self.scale = Scale(self.rect.size)
		self.elements.append (self.scale)
		
	def set_value (self, value):
		self.buffer.fill (C_KEY)
		value = value if value < 2 else 2
		value = value if value > -2 else -2
		m_y = (M_CENTRE - value) * self.scale.M_SPACING + 25
		pygame.draw.line (self.buffer, I_COLOR, (self.rect.w - 10, m_y), (self.rect.w - 10, 25+(M_CENTRE*self.scale.M_SPACING)), 12)
		