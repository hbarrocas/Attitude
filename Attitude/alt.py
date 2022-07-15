import pygame
import Attitude.base as b
import Attitude.tape as t
import Attitude.altgauge as gauge

F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_TAPE
F_COLOR = b.COLOR_MARKER
M_COLOR = b.COLOR_MARKER
M_COUNT = 10
M_CENTRE = 5  # M_COUNT / 2
M_SHORT = 8
M_LONG  = 20

C_KEY = b.COLOR_KEY


class Bug (b.Layer):

    def __init__ (self):
        super().__init__((15, 60))
        self.buffer.set_colorkey(C_KEY)
        self.buffer.fill (b.COLOR_CYAN)
        r = self.rect
        pygame.draw.polygon (self.buffer, C_KEY, [
            r.midleft, (r.right, r.centery-10),
            (r.right, r.centery+10), r.midleft
        ], 0)
        self.value = 0

    def set_value (self, value):
        self.value = float(value)/100
		

class ALT (b.Widget):

    def __init__ (self, sfc, rect):
        super().__init__(sfc, rect)
        tape_size = (rect.size[0], rect.size[1]*2)
        self.tape = t.Tape (tape_size, t.O_LEFT, t.DFL_ATTR)
        self.tape.scale.format = '{0:.1f}'
        self.tape.scale.m_value = lambda x : x * 0.1
        self.tape.ranges = [(-999, 999, 10, b.COLOR_DARKGREY)]
        self.centre_pos = self.rect.centery
        self.gauge = gauge.Display ((self.rect.w, 40))
        self.gauge.rect.midleft = (0, self.rect.centery)
        self.layers.append (self.tape)
        self.layers.append (self.gauge)
        self.set_value (0)

    def set_value (self, alt):
        alt = float(alt)
        #self.tape.set_value(alt/100)
        self.tape.set_centre (alt/100)
        self.tape.set_offset (self.centre_pos - self.tape.get_position(alt/100))
		
        self.gauge.set_value (alt)

    def set_index (self, value):
        self.tape.index_val = float(value)/100
