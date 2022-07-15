import pygame
import Attitude.base as b
import Attitude.tape as t
import Attitude.gauge as gauge

C_KEY = b.COLOR_KEY
F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_TAPE
F_COLOR = b.COLOR_TAPE_FG
F_COLOR_BG = b.COLOR_TAPE_BG
M_COLOR = b.COLOR_MARKER
M_COUNT = 10
M_CENTRE = 5  # M_COUNT / 2
M_SHORT = 8
M_LONG  = 20


class ASI (b.Widget):
    def __init__ (self, sfc, rect):
        super().__init__(sfc, rect)
        tape_size = (rect.width, rect.height*2)
        self.tape = t.Tape(tape_size, t.O_RIGHT, t.DFL_ATTR)
        self.tape.scale.m_value = lambda x : x * 10
        # Airspeed ranges (VS, VA, VNE, etc)
        self.tape.ranges[len(self.tape.ranges):] = [
            (0, 30, 15, b.COLOR_DARKGREY),
            (4.8, 12, 15, b.COLOR_GREEN),
            (4, 8.5, 6, (255,255,255)),
            (12, 14.8, 15, b.COLOR_YELLOW),
            (14.8, 999, 15, b.COLOR_RED)
        ]
        self.gauge = gauge.Display ((80, 40), gauge.O_RIGHT)
        self.gauge.rect.midright = (self.rect.right, self.rect.centery)
        self.layers.append(self.tape)
        self.layers.append(self.gauge)
        self.set_value (0)
		
    def set_value (self, ias):
        ias = float(ias)
        ias = 0 if ias < 0 else ias
        self.buffer.fill (F_COLOR_BG)
        self.tape.set_centre (ias/10 if ias > 40 else 4)
        self.tape.set_offset (self.rect.centery - self.tape.get_position(ias/10))
        self.gauge.set_value (str(int(ias)))
