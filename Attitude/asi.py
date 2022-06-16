import pygame
import base as b
import asigauge as gauge

FONT_SIZE = 28

M_COLOR = b.MKR_COLOR
M_COUNT = 10
M_CENTRE = 5  # M_COUNT / 2
M_SHORT = 10
M_LONG  = 25

COLOR_KEY = (0, 0, 0)

class Tape (b.EFISElement):

	def __init__ (self, dim):
		super().__init__((dim[0], dim[1]*2))
		self.M_SPACING = int(self.buffer.get_rect().h/M_COUNT)
		self.text = pygame.font.Font (b.FONT_FILE, FONT_SIZE)
		self.textarea = {}
		self.print_f = "{}"
		self.factor = 10
		self.ranges = [(0, 999999, (40, 40, 40))]
		self.m_layer = pygame.Surface (self.buffer.get_rect().size)
		self.m_layer.set_colorkey(COLOR_KEY)
		m_yl = range (0, self.buffer.get_rect().h, self.M_SPACING)
		m_ys = range (int(self.M_SPACING/2), self.buffer.get_rect().h, self.M_SPACING)
		for n in range(M_COUNT):
			pygame.draw.line (self.m_layer, M_COLOR, (self.rect.w, m_yl[n]), (self.rect.w - M_LONG, m_yl[n]), 2)
			pygame.draw.line (self.m_layer, M_COLOR, (self.rect.w, m_ys[n]), (self.rect.w - M_SHORT, m_ys[n]), 2)
		self.centre = 10
		self.set_value(0)
	
	def set_value (self, value):
		if value < self.centre -1 or value > self.centre + 1:
			# Set centre to nearest integer
			# Leave at 4 if value < 4 (scale lower end = 0)
			self.centre = int(value) if value > 4 else 4

			# reset range markers
			pygame.draw.line (self.buffer, COLOR_KEY, (self.rect.w - 6, 0), (self.rect.w - 6, self.rect.h), 12)
			for rg in self.ranges:
				m_b = int(self.M_SPACING * (M_CENTRE - rg[0] + self.centre))
				m_t = int(self.M_SPACING * (M_CENTRE - rg[1] + self.centre))
				pygame.draw.line (self.buffer, rg[2], (self.rect.w - 6, m_b), (self.rect.w - 6, m_t), 12)
				
			self.buffer.blit (self.m_layer, (0, 0))

			# reset marker numeric values
			val_range = range (self.centre+M_CENTRE, self.centre-M_CENTRE, -1)
			for n in range(M_COUNT):
				if n in self.textarea: self.buffer.fill (COLOR_KEY, self.textarea[n])
				label = self.print_f.format(val_range[n] * self.factor)
				fig = self.text.render (label, True, M_COLOR)
				r = fig.get_rect()
				r.midright = (self.rect.w - M_LONG - 5, self.M_SPACING * n)
				self.textarea[n] = self.buffer.blit (fig, r)
		
		# set tape offset relative to centre (target centery = M_CENTRE/2)
		self.rect.centery = int(self.M_SPACING * (M_CENTRE/2 - (self.centre - value)))
		

class ASI (b.EFISElement):
	def __init__ (self):
		super().__init__((100, 450))
		self.tape = Tape((100, 450))
		
		# Airspeed ranges (VS, VA, VNE, etc)
		self.tape.ranges[len(self.tape.ranges):] = [
			(4.8, 12, (0, 200, 0)),
			(12, 14.8, (200, 200, 0)),
			(14.8, 999, (200, 0, 0))
		]
		self.gauge = gauge.Display ()
		self.gauge.rect.midright = (self.rect.right, self.rect.centery)
		self.elements.append(self.tape)
		self.elements.append(self.gauge)
		self.set_value (0)
		
	def set_value (self, ias):
		ias = 0 if ias < 0 else ias
		self.tape.set_value (ias/10)
		self.gauge.set_value (ias)
