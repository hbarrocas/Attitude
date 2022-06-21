import pygame, math
import Attitude.base as b

SKY_COLOR = b.COLOR_SKY
GND_COLOR = b.COLOR_GND
M_COLOR_OVERLAY = b.COLOR_YELLOW
M_COLOR_HORIZON = b.COLOR_MARKER
M_LONG = 60
M_SHORT = 20
M_SPACING = 70
C_KEY = b.COLOR_KEY


class ATTIndOverlay (b.Layer):

	def __init__ (self, dim):
		super().__init__ (dim)
		self.buffer.set_colorkey(C_KEY)
		self.buffer.fill (C_KEY)
		r = self.buffer.get_rect()
		# Centre - aircraft "W" marking
		pygame.draw.lines (self.buffer, M_COLOR_OVERLAY, False, [
			(r.centerx-100, r.centery), (r.centerx-50, r.centery),
			(r.centerx-25, r.centery+25), r.center,
			(r.centerx+25, r.centery+25), (r.centerx+50, r.centery),
			(r.centerx+100, r.centery)
		], 4)
		# Top - Arrow, Roll angle indicator
		pygame.draw.polygon (self.buffer, M_COLOR_OVERLAY, [
			(r.centerx, r.centery-150), (r.centerx-10, r.centery-130),
			(r.centerx+10, r.centery-130), (r.centerx, r.centery-150)
		], 0)


class ATTIndHorizon (b.Layer):

	def __init__ (self, dim):
		super().__init__(dim)
		self.tape = pygame.Surface((int(dim[0]*1.5), dim[1]*6))
		area = self.tape.get_rect()
		area.height = area.centery
		self.tape.fill(SKY_COLOR, area)
		area.top = area.height
		self.tape.fill(GND_COLOR, area)
		pygame.draw.line (self.tape, M_COLOR_HORIZON, area.topleft, area.topright, 1)
		# Angle of pitch markers
		r = self.tape.get_rect()
		for mk_y in range (0, M_SPACING*10, M_SPACING):
			pygame.draw.line (self.tape, M_COLOR_HORIZON, (r.centerx-M_LONG, r.centery-mk_y), (r.centerx+M_LONG, r.centery-mk_y), 2)
			pygame.draw.line (self.tape, M_COLOR_HORIZON, (r.centerx-M_LONG, r.centery+mk_y), (r.centerx+M_LONG, r.centery+mk_y), 2)
		for mk_y in range (int(M_SPACING/2), M_SPACING*9, M_SPACING):
			pygame.draw.line (self.tape, M_COLOR_HORIZON, (r.centerx-M_SHORT, r.centery-mk_y), (r.centerx+M_SHORT, r.centery-mk_y), 2)
			pygame.draw.line (self.tape, M_COLOR_HORIZON, (r.centerx-M_SHORT, r.centery+mk_y), (r.centerx+M_SHORT, r.centery+mk_y), 2)
		# Angle of bank markings
		self.protractor = pygame.Surface((400, 400))
		self.protractor.set_colorkey (C_KEY)
		M_ANGLE = [
			0,
			math.pi/6,
			math.pi/3,
			5*math.pi/12,
			#math.pi/2,
			7*math.pi/12,
			2*math.pi/3,
			5*math.pi/6,
			math.pi
		]
		r = self.protractor.get_rect()
		for angle in M_ANGLE:
			pygame.draw.line (self.protractor, M_COLOR_HORIZON, b.radial(r.center, 150, angle), b.radial(r.center, 160, angle), 4)
		# Levelled bank marker (inverted triangle)
		pygame.draw.polygon (self.protractor, M_COLOR_HORIZON, [
			(r.centerx, r.centery-150), (r.centerx-10, r.centery-170),
			(r.centerx+10, r.centery-170), (r.centerx, r.centery-150)
		], 0)
		# Initialise
		self.set_attitude(0, 0)

	def set_attitude (self, aob, aop):
		hzn_r = self.tape.get_rect()
		hzn_r.height = hzn_r.width
		hzn_r.centery = self.tape.get_rect().centery - (aop * int(M_SPACING/10))
		rot_hzn = pygame.transform.rotate (self.tape.subsurface (hzn_r), aob)
		r = rot_hzn.get_rect()
		r.center = self.buffer.get_rect().center
		self.buffer.blit (rot_hzn, r)
		rot_prt = pygame.transform.rotate(self.protractor, aob)
		r = rot_prt.get_rect()
		r.center = self.buffer.get_rect().center
		self.buffer.blit (rot_prt, r)

class ATTInd (b.Widget):
	
	def __init__ (self, sfc, rect):
		super().__init__ (sfc, rect)
		# Fixed markings
		self.overlay = ATTIndOverlay (self.rect.size)
		self.horizon = ATTIndHorizon (self.rect.size)
		self.set_value ({"bank": 0, "pitch": 0})
		self.layers.append (self.horizon)
		self.layers.append (self.overlay)
	
	def set_value (self, value):
		self.horizon.set_attitude (float(value["bank"]), float(value["pitch"]))
		