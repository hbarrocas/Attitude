import pygame, sys
import base as b
from asi import ASI
from alt import ALT
from vsi import VSI
from attind import ATTInd
from compass import Compass
from sideslip import SlipIndicator
 
class EFIS:
	keymap = {}
	
	def __init__(self):
	
		# initialise graphics
		pygame.init()
		self.buffer = pygame.display.set_mode(b.EFIS_SIZE)

		self.altitude = 0
		self.airspeed = 0
		self.vspeed = 0
		self.pitch = 0
		self.bank = 0
		self.heading = 180
		self.slip = 0
					
		self.widgets = {}
		self.widgets["ASI"] = ASI ()
		self.widgets["ASI"].rect.topright = (100, 100)
		self.widgets["ALT"] = ALT ()
		self.widgets["ALT"].rect.topleft = (660, 100)
		self.widgets["VSI"] = VSI ()
		self.widgets["VSI"].rect.topright = (658, 100)		
		self.widgets["ATT"] = ATTInd ()
		self.widgets["ATT"].rect.midtop = (360, 100)
		self.widgets["HDG"] = Compass ()
		self.widgets["HDG"].rect.midbottom = (360, 80)
		self.widgets["HDG"].set_value(self.heading)
		self.widgets["SLI"] = SlipIndicator ()
		self.widgets["SLI"].rect.center = (360, 550)
		self.widgets["SLI"].set_value(self.slip)

		# Setup key bindings
		self.keymap = {
			pygame.K_UP: self.action_up,
			pygame.K_DOWN: self.action_down,
			pygame.K_LEFT: self.action_left,
			pygame.K_RIGHT: self.action_right,
			pygame.K_ESCAPE: self.exit
		}

	def action_left (self):
		self.bank -= 2
		self.heading -= 2
		self.slip -= 0.05

	def action_right (self):
		self.bank += 2
		self.heading += 2
		self.slip += 0.05

	def action_up (self):
		self.airspeed += 1
		self.altitude += 5
		self.pitch -= 1
		self.vspeed += 0.2

	def action_down (self):
		self.airspeed -= 1
		self.altitude -= 5
		self.pitch += 1
		self.vspeed -= 0.2
		
	def exit(self):
		pygame.quit()
		sys.exit(0)

	def refresh (self):
		for w in self.widgets:
			self.buffer.blit(self.widgets[w].surface (), self.widgets[w].rect)
		pygame.display.flip()
		
	def run(self):		
	
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key in self.keymap:
					self.keymap[event.key]()

			self.widgets["ASI"].set_value(self.airspeed)
			self.widgets["ALT"].set_value(self.altitude)
			self.widgets["VSI"].set_value(self.vspeed)
			self.widgets["ATT"].set_attitude(self.bank, self.pitch)
			self.widgets["HDG"].set_value(self.heading)
			self.widgets["SLI"].set_value(self.slip)
			self.refresh()

if __name__ == '__main__':
	E = EFIS()
	E.run()
