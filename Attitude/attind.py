import pygame, math
from base import EFISElement

class ATTIndOverlay (EFISElement):

	mk_color = (240, 240, 0)

	def __init__ (self, dim):
		super().__init__ (dim)
		self.buffer.set_colorkey((1, 1, 1))
		self.buffer.fill ((1, 1, 1))
		r = self.buffer.get_rect()
		# Centre - aircraft "W" marking
		pygame.draw.lines (self.buffer, self.mk_color, False, [
			(r.centerx-100, r.centery), (r.centerx-50, r.centery),
			(r.centerx-25, r.centery+25), r.center,
			(r.centerx+25, r.centery+25), (r.centerx+50, r.centery),
			(r.centerx+100, r.centery)
		], 4)
		# Top - Arrow, Roll angle indicator
		pygame.draw.polygon (self.buffer, self.mk_color, [
			(r.centerx, r.centery-150), (r.centerx-10, r.centery-130),
			(r.centerx+10, r.centery-130), (r.centerx, r.centery-150)
		], 0)

class ATTIndHorizon (EFISElement):

	sky_color = (80, 100, 180)
	gnd_color = (160, 90, 0)
	mk_color = (200, 200, 200)
	mk_spacing = 80
	mk_long = 75
	mk_short = 25

	def __init__ (self, dim):
		super().__init__(dim)
		self.tape = pygame.Surface((int(dim[0]*1.5), dim[1]*6))
		area = self.tape.get_rect()
		area.height = area.centery
		self.tape.fill(self.sky_color, area)
		area.top = area.height
		self.tape.fill(self.gnd_color, area)
		pygame.draw.line (self.tape, self.mk_color, area.topleft, area.topright, 1)
		# Angle of pitch markers
		r = self.tape.get_rect()
		for mk_y in range (0, self.mk_spacing*10, self.mk_spacing):
			pygame.draw.line (self.tape, self.mk_color, (r.centerx-self.mk_long, r.centery-mk_y), (r.centerx+self.mk_long, r.centery-mk_y), 2)
			pygame.draw.line (self.tape, self.mk_color, (r.centerx-self.mk_long, r.centery+mk_y), (r.centerx+self.mk_long, r.centery+mk_y), 2)
		for mk_y in range (int(self.mk_spacing/2), self.mk_spacing*9, self.mk_spacing):
			pygame.draw.line (self.tape, self.mk_color, (r.centerx-self.mk_short, r.centery-mk_y), (r.centerx+self.mk_short, r.centery-mk_y), 2)
			pygame.draw.line (self.tape, self.mk_color, (r.centerx-self.mk_short, r.centery+mk_y), (r.centerx+self.mk_short, r.centery+mk_y), 2)
		# Angle markings
		self.mk_aob = pygame.Surface((400, 400))
		self.mk_aob.set_colorkey ((0, 0, 0))
		mk_angle = [
			0,
			math.pi/6,
			math.pi/3,
			5*math.pi/12,
			math.pi/2,
			7*math.pi/12,
			2*math.pi/3,
			5*math.pi/6,
			math.pi
		]
		r = self.mk_aob.get_rect()
		for angle in mk_angle:
			pygame.draw.line (self.mk_aob, self.mk_color, self.radial(r.center, 150, angle), self.radial(r.center, 160, angle), 4)
		# Initialise
		self.set_attitude(0, 0)


	def radial (self, centre, radius, angle):
		return (centre[0]+radius*math.cos(angle), centre[1]-radius*math.sin(angle))
            
	def set_attitude (self, aob, aop):
		att_r = self.tape.get_rect()
		att_r.height = att_r.width
		att_r.centery = self.tape.get_rect().centery - (aop * int(self.mk_spacing/10))
		att = pygame.transform.rotate (self.tape.subsurface (att_r), aob)
		r = att.get_rect()
		r.center = self.buffer.get_rect().center
		self.buffer.blit (att, r)
		rot_aob = pygame.transform.rotate(self.mk_aob, aob)
		r = rot_aob.get_rect()
		r.center = self.buffer.get_rect().center
		self.buffer.blit (rot_aob, r)

class ATTInd (EFISElement):
	
	def __init__ (self):
		super().__init__ ((450, 450))
		self.buffer.fill ((40, 40, 40))
		# Fixed markings
		self.overlay = ATTIndOverlay (self.rect.size)
		self.horizon = ATTIndHorizon (self.rect.size)
		self.set_attitude (0, 0)
		self.elements.append (self.horizon)
		self.elements.append (self.overlay)
	
	def set_attitude (self, aob, aop):
		self.horizon.set_attitude (aob, aop)
		