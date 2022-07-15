import pygame
import Attitude.base as b

DFL_ATTR = {
        'length': 8,
        'subdv': 2,
        'f_size': 24,
        'f_color': (200, 200, 200),
        'i_color': b.COLOR_MAGENTA,
        'm_long': 20,
        'm_short': 10,
        'm_color': (200, 200, 200)
}

O_LEFT = 1
O_RIGHT = 2
O_TOP = 3
O_BOTTOM = 4

T_COLOR_BG = (0, 0, 0)
T_COLOR_FG = (200, 200, 200)

C_KEY = (0, 0, 0)

# area_dim returns tuple representing graphic area dimensions based on orientation
# of the scale or tape, and its size (width, length)
def area_dim (size, orient):
    return size if orient == O_LEFT or orient == O_RIGHT else (size[1], size[0])


class Index (b.Layer):

    def __init__ (self, orient, colour):
        super().__init__(area_dim((16, 60), orient))
        self.buffer.set_colorkey(C_KEY)
        self.buffer.fill (colour)
        self.orient = orient
        r = self.rect
        poly = {
            O_LEFT: [r.midleft, (r.right, r.centery-10), (r.right, r.centery+10), r.midleft],
            O_RIGHT: [r.midright, (r.left, r.centery-10), (r.left, r.centery+10), r.midright],
            O_TOP: [r.midtop, (r.centerx-10, r.bottom), (r.centerx+10, r.bottom), r.midtop],
            O_BOTTOM: [r.midbottom, (r.centerx-10, r.top), (r.centerx+10, r.top), r.midbottom]
        }
        pygame.draw.polygon (self.buffer, C_KEY, poly[orient], 0)


class Scale (b.Layer):
    # size = (width, length) in pixels
    def __init__ (self, size, orient, attr):
        super().__init__(area_dim(size, orient))
        self.buffer.set_colorkey(C_KEY)
        self.txt = pygame.font.Font (b.FONT_FILE, attr['f_size'])
        self.txt_area = {}

        self._start_value = 0
		
        self.attr = attr
        self.format = '{}'
        self.m_value = lambda x : x
        self.factor = 1
        self.orient = orient
        self.padding = attr['f_size']
        self.spacing = int((size[1]-2*self.padding)/attr['length'])
        #self.position = range (self.padding, (self.spacing * attr['length'])+self.padding, self.spacing)
        self.position = range (self.padding, size[1], self.spacing)
		
        m_beg = 0 if orient == O_LEFT or orient == O_TOP else size[0]
        for m in range(attr['length']):
            for n in range (attr['subdv']):
                m_length = attr['m_short'] if n else attr['m_long']
                m_end = m_length if orient == O_LEFT or orient == O_TOP else size[0] - m_length
                m_pos = self.position[m] + int((n * self.spacing) / attr['subdv'])
                if orient == O_LEFT or orient == O_RIGHT:
                    pygame.draw.line (self.buffer, attr['m_color'], (m_beg, m_pos), (m_end, m_pos), 2)
                elif orient == O_TOP or orient == O_BOTTOM:
                    pygame.draw.line (self.buffer, attr['m_color'], (m_pos, m_beg), (m_pos, m_end), 2)

    @property
    def start_value (self):
        return self._start_value

    @start_value.setter
    def start_value (self, value):
        value = int(value) + self.attr['length'] if self.orient == O_LEFT or self.orient == O_RIGHT else int(value)
        for n in range (self.attr['length']):
            if n in self.txt_area: self.buffer.fill (C_KEY, self.txt_area[n])
            number = value-n if self.orient == O_RIGHT or self.orient == O_LEFT else value+n
            fig = self.txt.render (self.format.format(self.m_value(number)), True, T_COLOR_FG)
            r = fig.get_rect()
            if self.orient == O_LEFT: r.midleft = (self.attr['m_long']+5, self.position[n])
            elif self.orient == O_RIGHT: r.midright = (self.rect.w-self.attr['m_long']-5, self.position[n])
            elif self.orient == O_TOP: r.midtop = (self.position[n], self.attr['m_long']+5)
            elif self.orient == O_BOTTOM: r.midbottom = (self.position[n], self.rect.h-self.attr['m_long']-5)
            self.txt_area[n] = self.buffer.blit (fig, r)


class Tape (b.Layer):
    # size = (width, length) in pixels
    def __init__ (self, size, orient, attr):
        super().__init__(area_dim(size, orient))		
        self.scale = Scale (size, orient, attr)
        self.index = Index (orient, attr['i_color'])
        self.ranges = [] # = [(0, 99999, 12, b.COLOR_DARKGREY)]
        self.index_val = 0
        self.centre_pos = self.scale.position[int(self.scale.attr['length']/2)]
        self.centre_val = 0
        self.layers.append (self.scale)
        self.layers.append (self.index)
	
    def set_offset (self, offset):
        self.rect.left = offset if self.scale.orient == O_TOP or self.scale.orient == O_BOTTOM else 0
        self.rect.top = offset if self.scale.orient == O_LEFT or self.scale.orient == O_RIGHT else 0
	
    def get_position (self, value):
        if self.scale.orient == O_LEFT or self.scale.orient == O_RIGHT:
            return self.centre_pos - (value - self.centre_val)*self.scale.spacing
        else:
            return self.centre_pos + (value - self.centre_val)*self.scale.spacing
	
    def set_centre (self, value):
        # clear the tape
        self.buffer.fill (T_COLOR_BG)
        # Centre marker is the closest integer value
        self.centre_val = int(value)
        # reset scale with new centre value
        self.scale.start_value = self.centre_val - (int(self.scale.attr['length']/2))
        # redraw all visible range markers
        for m in self.ranges:
            if self.scale.orient == O_TOP or self.scale.orient == O_BOTTOM:
                x1 = self.get_position(m[0])
                x2 = self.get_position(m[1])
                y1 = y2 = 4 if self.scale.orient == O_TOP else self.rect.bottom - 5
            if self.scale.orient == O_LEFT or self.scale.orient == O_RIGHT:
                y1 = self.get_position(m[0])
                y2 = self.get_position(m[1])
                x1 = x2 = 4 if self.scale.orient == O_LEFT else self.rect.right - 5
            pygame.draw.line (self.buffer, m[3], (x1, y1), (x2, y2), m[2])
        # Position the index
        if self.scale.orient == O_LEFT or self.scale.orient == O_RIGHT:
            self.index.rect.centery = self.get_position(self.index_val)
            self.index.rect.centerx = 8 if self.scale.orient == O_LEFT else self.rect.w - 8
        else:
            self.index.rect.centerx = self.get_position(self.index_val)
            self.index.rect.centery = 8 if self.scale.orient == O_TOP else self.rect.h - 8
