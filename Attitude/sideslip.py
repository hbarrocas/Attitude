import pygame
import base as b

COLOR_KEY = (0, 0, 0)

FRAME_COLOR = b.MKR_COLOR
FRAME_BKGND = (40, 40, 40)
BALL_COLOR = (150, 150, 150)

class SlipBall (b.EFISElement):

	def __init__ (self, radius):
		super().__init__((radius*2, radius*2))
		self.buffer.set_colorkey (COLOR_KEY)
		pygame.draw.circle (self.buffer, BALL_COLOR, self.rect.center, radius, 0)

	def offset (self, offset):
		self.rect.left = offset

class Frame (b.EFISElement):

	def __init__ (self, dim):
		super().__init__(dim)
		r = self.rect
		self.buffer.set_colorkey (COLOR_KEY)
		#pygame.draw.polygon (self.buffer, FRAME_COLOR, [
		#	r.topleft, (r.right-1, r.top), (r.right-1, r.bottom-1),
		#	(r.left, r.bottom-1), r.topleft
		#], 1)
		pygame.draw.line (self.buffer, FRAME_COLOR, (r.centerx-int(r.height/2), r.top), (r.centerx-int(r.height/2), r.bottom), 2)
		pygame.draw.line (self.buffer, FRAME_COLOR, (r.centerx+int(r.height/2), r.top), (r.centerx+int(r.height/2), r.bottom), 2)

		
class SlipIndicator (b.EFISElement):
	
	def __init__ (self):
		super().__init__((200, 30))
		# Instrument frame and markings
		self.buffer.fill(FRAME_BKGND)
		self.frame = Frame (self.rect.size)
		# Slip ball - centered = 0
		self.ball = SlipBall (int(self.rect.h/2)-2)
		self.elements.append(self.ball)
		self.elements.append(self.frame)
		
	def set_value (self, value):
		value = value if value < 1 else 1
		value = value if value > -1 else -1
		self.ball.offset ((value + 1) * int((self.rect.w - self.ball.rect.w)/2))
		self.buffer.fill(FRAME_BKGND)
		
