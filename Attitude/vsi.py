import pygame
import base as b

COLOR_KEY = (0, 0, 0)

M_COLOR = b.MKR_COLOR
M_SHORT = 12
M_LONG = 25
M_COUNT = 4
M_CENTRE = 2

VAL_COLOR = (200, 40, 150)

FONT_COLOR = b.MKR_COLOR
FONT_SIZE = 25

class Scale (b.EFISElement):

	def __init__ (self, dim):
		super().__init__(dim)
		self.buffer.set_colorkey(COLOR_KEY)
		self.M_SPACING = int((self.rect.h - 50)/M_COUNT)
		self.text = pygame.font.Font (b.FONT_FILE, FONT_SIZE)
		pygame.draw.line (self.buffer, M_COLOR, (self.rect.w-2, 25), (self.rect.w-2, self.rect.h-25), 2)
		m_yl = range (25, self.rect.h, self.M_SPACING)
		m_ys = range (25+int(self.M_SPACING/2), self.rect.h, self.M_SPACING)
		for n in range(M_COUNT+1):
			pygame.draw.line (self.buffer, M_COLOR, (self.rect.w, m_yl[n]), (self.rect.w-M_LONG, m_yl[n]), 2)
			fig = self.text.render (str(M_CENTRE-n), True, FONT_COLOR)
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
		self.buffer.fill (COLOR_KEY)
		value = value if value < 2 else 2
		value = value if value > -2 else -2
		m_y = (M_CENTRE - value) * self.scale.M_SPACING + 25
		pygame.draw.line (self.buffer, VAL_COLOR, (self.rect.w - 10, m_y), (self.rect.w - 10, 25+(M_CENTRE*self.scale.M_SPACING)), 12)
		