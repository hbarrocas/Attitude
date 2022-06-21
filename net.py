#!/usr/bin/env python3

from Attitude.pfd import PFD
import socket, pygame, json

pygame.init()
display = pygame.display.set_mode((800, 800))

p = PFD (display, display.get_rect())
p.set_value({})
p.render()
pygame.display.flip()

while 1:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind (('localhost', 12345))
	s.listen (1)

	conn, addr = s.accept()

	data = conn.recv(1024)
	while len(data) > 0:
		values = json.loads(data)
		p.set_value(values)
		p.render()
		pygame.display.flip()
		data = conn.recv(1024)

	conn.close()
	# With no connection - show disabled instrumentation
	p.set_value({})
	p.render()
	pygame.display.flip()
	
pygame.quit()