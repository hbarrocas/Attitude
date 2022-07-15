import pygame
import Attitude.base as b
import Attitude.gauge as gauge

F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_GAUGE
R_SIZE = int(b.FONT_SIZE_GAUGE*3/4)
F_COLOR_FG = b.COLOR_GAUGE_FG
F_COLOR_BG = b.COLOR_GAUGE_BG
C_KEY = b.COLOR_KEY


class DisplayRoller (b.Layer):

    def __init__ (self):
        super().__init__((40, R_SIZE * 6))
        self.buffer.fill (F_COLOR_BG, self.rect)
        self.text = pygame.font.Font (F_FILE, R_SIZE)
        num_y = range (0, R_SIZE*6, R_SIZE)
        for n in range(6):
            fig = self.text.render ("{0:0>2}".format((n % 5)*20), True, F_COLOR_FG)
            r = fig.get_rect()
            r.top = num_y[n]
            self.buffer.blit (fig, r)

    def set_value (self, value):
        offset = (value % 100) / 20
        self.rect.top = (-offset if value > 0 else -5+offset) * R_SIZE + 4


class Display (gauge.Display):

    def __init__ (self, size):
        super().__init__(size, gauge.O_LEFT)
        fld_r = self.display.get_rect()
        fld_r.width = 60
        #fld_r.topleft = (0, 0)
        self.display = self.display.subsurface(fld_r)
        r = self.buffer.get_rect()
        rd_r = pygame.Rect((0, 0), (32, 18))
        rd_r.topright = (r.right-4, r.top+8)
        self.buffer.set_clip (rd_r)
        self.roller = DisplayRoller()
        self.roller.rect = rd_r
        self.layers.append (self.roller)		

    def set_value (self, value):
        self.roller.set_value (value)
        super().set_value(str(int(value/100)))
