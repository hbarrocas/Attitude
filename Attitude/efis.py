import pygame, sys
import Attitude.base as b
from Attitude.asi import ASI
from Attitude.alt import ALT
from Attitude.vsi import VSI
from Attitude.attind import ATTInd
from Attitude.compass import Compass
from Attitude.sideslip import SlipIndicator

EFIS_SIZE = (800, 800)
EFIS_MAP_POSITION = {
	"ASI": (5, 100),
	"ALT": (660, 100),
	"VSI": (600, 100),
	"ATT": (125, 100),
	"HDG": (125, 20),
	"SSI": (250, 530)
}

buffer = False
widget = {}

def init():
	global buffer
	global widget
	# initialise graphics
	pygame.init()
	buffer = pygame.display.set_mode(EFIS_SIZE)
	widget = {}
	widget["ASI"] = ASI ()
	widget["ALT"] = ALT ()
	widget["VSI"] = VSI ()
	widget["ATT"] = ATTInd ()
	widget["HDG"] = Compass ()
	widget["SSI"] = SlipIndicator ()
	for w in widget: widget[w].rect.topleft = EFIS_MAP_POSITION[w]

def set_value (value):
	global widget
	for w in widget:
		if w not in value: widget[w].disable()
		else:
			widget[w].enable()
			widget[w].set_value(value[w])
				
def quit ():
	pygame.quit ()
	
def refresh ():
	global buffer
	global widget
	for w in widget:
		buffer.blit(widget[w].surface (), widget[w].rect)
	pygame.display.flip()
		