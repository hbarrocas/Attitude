import pygame
import base as b

FONT_COLOR = b.MKR_COLOR
FONT_BKGND = (40, 40, 40)
FRAME_COLOR = (200, 200, 200)

MKR_LONG = 25
MKR_SHORT = 12
MKR_COUNT = 24
MKR_CENTRE = int(MKR_COUNT/2)

COLOR_KEY = (0, 0, 0)

class Tape (b.EFISElement):

	FONT_SIZE = 28
	
	def __init__ (self, dim):
		self.MKR_SPACING = int(dim[0]/12)
		super().__init__((self.MKR_SPACING * MKR_COUNT, dim[1]))
		self.text = pygame.font.Font (b.FONT_FILE, self.FONT_SIZE)
		self.textarea = {}
		for mkr_n in range (MKR_COUNT):
			mkr_x = mkr_n * self.MKR_SPACING
			mkr_y = MKR_SHORT if mkr_n % 3 else MKR_LONG
			pygame.draw.line (self.buffer, b.MKR_COLOR, (mkr_x, self.rect.bottom), (mkr_x, self.rect.bottom-mkr_y), 2)
		self.centre = 0
		self.set_value(0)

	def set_value (self, value):
		value = value/10
		self.centre = int(value) if int(value) % 3 == 0 else self.centre 
		val_range = range (self.centre-MKR_CENTRE, self.centre+MKR_CENTRE, 3)
		val_pos = range (0, self.MKR_SPACING * MKR_COUNT, self.MKR_SPACING*3)
		for n in range (len(val_pos)):
			if n in self.textarea: self.buffer.fill (COLOR_KEY, self.textarea[n])
			fig = self.text.render ("{0:02d}".format((val_range[n]+36)%36), True, FONT_COLOR)
			r = fig.get_rect()
			r.midbottom = (val_pos[n], self.rect.bottom - MKR_LONG - 5)
			self.textarea[n] = self.buffer.blit(fig, r)
			
		self.rect.centerx = int(self.MKR_SPACING * (MKR_CENTRE/2 + (self.centre-value)))

			
class Display (b.EFISElement):
	
	FONT_SIZE = 40

	def __init__ (self):
		super().__init__((90, 60))
		self.buffer.set_colorkey (COLOR_KEY)
		self.buffer.fill (COLOR_KEY)
		self.text = pygame.font.Font (b.FONT_FILE, self.FONT_SIZE)
		# Frame with pointer
		r = self.buffer.get_rect()
		pygame.draw.polygon (self.buffer, FRAME_COLOR, [
			r.midbottom, (r.centerx+10, r.bottom-14),
			(r.right-2, r.bottom-14), (r.right-2, r.top),
			r.topleft, (r.left, r.bottom-14),
			(r.centerx-10, r.bottom-14), r.midbottom
		], 0)
		pygame.draw.polygon (self.buffer, FONT_BKGND, [
			(r.centerx, r.bottom-4), (r.centerx+10, r.bottom-17),
			(r.centerx-10, r.bottom-17), (r.centerx, r.bottom-4)
		], 0)
		r.size = (r.width - 5, r.height - 17)
		r.topleft = (2, 2)
		self.buffer.set_clip (r)
		
	def set_value (self, value):
		fig = self.text.render ("{0:03d}".format(value % 360), True, FONT_COLOR)
		r = fig.get_rect()
		r.centerx = self.buffer.get_rect().centerx
		self.buffer.fill (FONT_BKGND)
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
		
	def set_value (self, value):
		self.tape.set_value(value)
		self.gauge.set_value(value)

