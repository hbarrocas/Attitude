import pygame
import Attitude.altgauge as gauge
import Attitude.base as b

F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_TAPE
F_COLOR = b.COLOR_MARKER
M_COLOR = b.COLOR_MARKER
M_COUNT = 10
M_CENTRE = 5  # M_COUNT / 2
M_SHORT = 8
M_LONG  = 20

C_KEY = b.COLOR_KEY


class Bug (b.Layer):

	def __init__ (self):
		super().__init__((15, 60))
		self.buffer.set_colorkey(C_KEY)
		self.buffer.fill (b.COLOR_CYAN)
		r = self.rect
		pygame.draw.polygon (self.buffer, C_KEY, [
			r.midleft, (r.right, r.centery-10),
			(r.right, r.centery+10), r.midleft
		], 0)
		self.value = 0

class Tape (b.Layer):

	def __init__ (self, dim):
		super().__init__((dim[0], dim[1]*2))
		self.M_SPACING = int(self.buffer.get_rect().h/M_COUNT)
		self.text = pygame.font.Font (F_FILE, F_SIZE)
		self.textarea = {}
		self.print_f = "{0:.1f}"
		self.factor = 0.1
		self.ranges = [(-99999, 999999, b.COLOR_DARKGREY)]
		self.m_layer = pygame.Surface (self.buffer.get_rect().size)
		self.m_layer.set_colorkey(C_KEY)
		m_yl = range (0, self.buffer.get_rect().h, self.M_SPACING)
		m_ys = range (int(self.M_SPACING/2), self.buffer.get_rect().h, self.M_SPACING)
		for n in range(M_COUNT):
			pygame.draw.line (self.m_layer, M_COLOR, (0, m_yl[n]), (M_LONG, m_yl[n]), 2)
			pygame.draw.line (self.m_layer, M_COLOR, (0, m_ys[n]), (M_SHORT, m_ys[n]), 2)
		self.bug = Bug ()
		self.layers.append (self.bug)
		self.centre = 10
		self.bug.value = 1
		self.set_value(0)
	
	def set_value (self, value):
		if value < self.centre -1 or value > self.centre + 1:
			# Set to nearest integer
			self.centre = int(value)

			# reset range markers
			pygame.draw.line (self.buffer, C_KEY, (6, 0), (6, self.rect.h), 20)
			for rg in self.ranges:
				m_b = int(self.M_SPACING * (M_CENTRE - rg[0] + self.centre))
				m_t = int(self.M_SPACING * (M_CENTRE - rg[1] + self.centre))
				pygame.draw.line (self.buffer, rg[2], (6, m_b), (6, m_t), 12)
				
			self.buffer.blit (self.m_layer, (0, 0))
		
			# reset marker numeric values
			val_range = range (self.centre+M_CENTRE, self.centre-M_CENTRE, -1)
			for n in range(M_COUNT):
				if n in self.textarea: self.buffer.fill (C_KEY, self.textarea[n])
				label = self.print_f.format(val_range[n] * self.factor)
				fig = self.text.render (label, True, F_COLOR)
				r = fig.get_rect()
				r.midleft = (M_LONG + 5, self.M_SPACING * n)
				self.textarea[n] = self.buffer.blit (fig, r)
		
		# set tape offset relative to centre (target centery = M_CENTRE/2)
		self.rect.centery = int(self.M_SPACING * (M_CENTRE/2 - (self.centre - value)))
		# reset bug position
		self.bug.rect.centery = int(self.M_SPACING * (M_CENTRE - self.bug.value + self.centre))
		

class ALT (b.Widget):
	def __init__ (self, sfc, rect):
		super().__init__(sfc, rect)
		self.tape = Tape(self.rect.size)
		self.gauge = gauge.Display ()
		self.gauge.rect.midleft = (0, self.rect.centery)
		self.layers.append (self.tape)
		self.layers.append (self.gauge)
		self.set_value (0)

	def set_bug (self, alt):
		self.tape.bug.value = alt/100
				
	def set_value (self, alt):
		self.tape.set_value(alt/100)
		self.gauge.set_value (alt)
