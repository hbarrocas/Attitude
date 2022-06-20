import pygame
import Attitude.base as b
from Attitude.display import Baro, GSpeed
from Attitude.asi import ASI
from Attitude.alt import ALT
from Attitude.vsi import VSI
from Attitude.attind import ATTInd
from Attitude.compass import Compass
from Attitude.sideslip import SlipIndicator

SIZE = (800, 800)

class PFD (b.Widget):

	def __init__(self, sfc, rect):
		super().__init__(sfc, rect)
		self.widget = {
			"ASI": ASI (self.buffer, pygame.Rect((80, 100), (80, 400))),
			"ALT": ALT (self.buffer, pygame.Rect((660, 100), (110, 400))),
			"BARO": Baro(self.buffer, pygame.Rect((620, 510), (130, 42))),
			"GS": GSpeed(self.buffer, pygame.Rect((80, 510), (90, 42))),
			"VSI": VSI (self.buffer, pygame.Rect((605, 100), (50, 400))),
			"ATT": ATTInd (self.buffer, pygame.Rect((200, 100), (400, 400))),
			"HDG": Compass (self.buffer, pygame.Rect((200, 20), (400, 50))),
			"SSI": SlipIndicator (self.buffer, pygame.Rect((300, 510), (200, 30)))
		}

	def set_value (self, value):
		for x in self.widget:
			if x not in value: self.widget[x].disable()
			else:
				self.widget[x].enable()
				self.widget[x].set_value(value[x])
			self.widget[x].render()
			