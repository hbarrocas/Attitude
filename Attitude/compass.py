import pygame, copy
import Attitude.base as b
import Attitude.tape as t
import Attitude.gauge as gauge

F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_TAPE
F_COLOR_FG = b.COLOR_TAPE_FG
F_COLOR_BG = b.COLOR_TAPE_BG

G_SIZE = b.FONT_SIZE_GAUGE
G_COLOR_FG = b.COLOR_GAUGE_FG
G_COLOR_BG = b.COLOR_GAUGE_BG

M_COLOR = b.COLOR_MARKER
M_LONG = 20
M_SHORT = 8
M_COUNT = 24
M_CENTRE = int(M_COUNT/2)

C_KEY = (0, 0, 0)


class Bug (b.Layer):

    def __init__ (self):
        super().__init__((60, 15))
        self.buffer.set_colorkey(C_KEY)
        self.buffer.fill (b.COLOR_CYAN)
        r = self.rect
        pygame.draw.polygon (self.buffer, C_KEY, [
            r.midbottom, (r.centerx-10, r.top),
            (r.centerx+10, r.top), r.midbottom
        ], 0)
        self.value = 0

    def set_value (self, value):
        self.value = int(float(value)) % 360
		

class Compass (b.Widget):
	
    def __init__ (self, sfc, rect):
        super().__init__ (sfc, rect)
        tape_size = (rect.height, rect.width*2)
        attr = copy.deepcopy(t.DFL_ATTR)
        attr['length'] = 6
        attr['subdv'] = 3
        self.tape = t.Tape(tape_size, t.O_BOTTOM, attr)
        self.tape.scale.format = '{0:02d}'
        self.tape.scale.m_value = lambda x : ((x * 3)+36)%36
        self.gauge = gauge.Display ((70, 50), gauge.O_DOWN)
        self.gauge.rect.midbottom = self.rect.midbottom
        self.layers.append(self.tape)
        self.layers.append(self.gauge)
        self.set_value(0)
		
    def set_value (self, value):
        value = float(value)
        self.tape.set_centre (value/30)
        self.tape.set_offset (self.rect.centerx - self.tape.get_position(value/30))
        self.gauge.set_value("{0:03d}".format(int(value%360)))

    def set_index (self, value):
        self.tape.index_val = float(value)/30
