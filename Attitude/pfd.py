import pygame
import Attitude.base as b
import Attitude.display as display
from Attitude.asi import ASI
from Attitude.alt import ALT
from Attitude.vsi import VSI
from Attitude.attind import ATTInd
from Attitude.compass import Compass
from Attitude.sideslip import SlipIndicator

SIZE = (800, 800)
MAP_POSITION = {
	"ASI": (80, 100),
	"ALT": (660, 100),
	"BARO": (620, 510),
	"GS": (80, 510),
	"VSI": (605, 100),
	"ATT": (200, 100),
	"HDG": (200, 20),
	"SSI": (300, 510),
}


class PFD (b.EFISElement):

	def __init__(self):
		super().__init__(SIZE)
		self.widget = {
			"ASI": ASI (),
			"ALT": ALT (),
			"BARO": display.Baro(),
			"GS": display.GSpeed(),
			"VSI": VSI (),
			"ATT": ATTInd (),
			"HDG": Compass (),
			"SSI": SlipIndicator ()
		}
		for x in self.widget:
			self.widget[x].rect.topleft = MAP_POSITION[x]

	def set_value (self, value):
		for x in self.widget:
			if x not in value: self.widget[x].disable()
			else:
				self.widget[x].enable()
				self.widget[x].set_value(value[x])

	def surface (self):
		for x in self.widget:
			self.buffer.blit(self.widget[x].surface(), self.widget[x].rect)
		return self.buffer
		