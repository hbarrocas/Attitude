import pygame
import Attitude.base as b

F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_TAPE
F_COLOR_FG = b.COLOR_TAPE_FG
F_COLOR_BG = b.COLOR_TAPE_BG

G_SIZE = b.FONT_SIZE_GAUGE
G_COLOR_FG = b.COLOR_GAUGE_FG
G_COLOR_BG = b.COLOR_GAUGE_BG

M_COLOR = b.COLOR_MARKER
M_LONG = 25
M_SHORT = 12
M_COUNT = 24
M_CENTRE = int(M_COUNT/2)

C_KEY = (0, 0, 0)


class Tape (b.EFISElement):

	def __init__ (self, dim):
		self.M_SPACING = int(dim[0]/12)
		super().__init__((self.M_SPACING * M_COUNT, dim[1]))
		self.text = pygame.font.Font (F_FILE, F_SIZE)
		self.textarea = {}
		for mkr_n in range (M_COUNT):
			mkr_x = mkr_n * self.M_SPACING
			mkr_y = M_SHORT if mkr_n % 3 else M_LONG
			pygame.draw.line (self.buffer, M_COLOR, (mkr_x, self.rect.bottom), (mkr_x, self.rect.bottom-mkr_y), 2)
		self.centre = 0
		self.set_value(0)

	def set_value (self, value):
		value = value/10
		self.centre = int(value) if int(value) % 3 == 0 else self.centre 
		val_range = range (self.centre-M_CENTRE, self.centre+M_CENTRE, 3)
		val_pos = range (0, self.M_SPACING * M_COUNT, self.M_SPACING*3)
		for n in range (len(val_pos)):
			if n in self.textarea: self.buffer.fill (C_KEY, self.textarea[n])
			fig = self.text.render ("{0:02d}".format((val_range[n]+36)%36), True, F_COLOR_FG)
			r = fig.get_rect()
			r.midbottom = (val_pos[n], self.rect.bottom - M_LONG - 5)
			self.textarea[n] = self.buffer.blit(fig, r)
			
		self.rect.centerx = int(self.M_SPACING * (M_CENTRE/2 + (self.centre-value)))

			

class Display (b.EFISElement):
	
	def __init__ (self):
		super().__init__((90, 60))
		self.buffer.set_colorkey (C_KEY)
		self.buffer.fill (C_KEY)
		self.text = pygame.font.Font (F_FILE, G_SIZE)
		# Frame with pointer
		r = self.buffer.get_rect()
		pygame.draw.polygon (self.buffer, G_COLOR_FG, [
			r.midbottom, (r.centerx+10, r.bottom-14),
			(r.right-2, r.bottom-14), (r.right-2, r.top),
			r.topleft, (r.left, r.bottom-14),
			(r.centerx-10, r.bottom-14), r.midbottom
		], 0)
		pygame.draw.polygon (self.buffer, G_COLOR_BG, [
			(r.centerx, r.bottom-4), (r.centerx+10, r.bottom-17),
			(r.centerx-10, r.bottom-17), (r.centerx, r.bottom-4)
		], 0)
		r.size = (r.width - 5, r.height - 17)
		r.topleft = (2, 2)
		self.buffer.set_clip (r)		

	def set_value (self, value):
		fig = self.text.render ("{0:03d}".format(value % 360), True, G_COLOR_FG)
		r = fig.get_rect()
		r.centerx = self.buffer.get_rect().centerx
		self.buffer.fill (G_COLOR_BG)
		self.buffer.blit (fig, r)

		
class Compass (b.EFISElement):
	
	def __init__ (self):
		super().__init__ ((450, 60))
		#self.buffer.set_colorkey(COLOR_KEY)
		self.tape = Tape(self.rect.size)
		self.gauge = Display ()
		self.gauge.rect.midbottom = self.rect.midbottom
		self.elements.append(self.tape)
		self.elements.append(self.gauge)
		self.set_value(0)
		
	def set_value (self, value):
		self.tape.set_value(value)
		self.gauge.set_value(value)

