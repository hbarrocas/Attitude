import pygame
import Attitude.base as b

F_FILE = b.FONT_FILE
F_SIZE = b.FONT_SIZE_GAUGE
F_COLOR_FG = b.COLOR_GAUGE_FG
F_COLOR_BG = b.COLOR_GAUGE_BG
C_KEY = b.COLOR_KEY

O_RIGHT = 1
O_LEFT  = 2
O_DOWN  = 3
O_UP    = 4

G_SIZE_POINTER = 12


class Display (b.Layer):

    def __init__ (self, size, ori):
        super().__init__(size)
        self.buffer.set_colorkey (C_KEY)
        self.buffer.fill (C_KEY)
        self.text = pygame.font.Font (F_FILE, F_SIZE)
        r = self.buffer.get_rect()
        r.height = r.height if ori == O_RIGHT or ori == O_LEFT else r.height-G_SIZE_POINTER
        r.width = r.width if ori == O_UP or ori == O_DOWN else r.width-G_SIZE_POINTER
        if ori == O_LEFT or ori == O_UP: r.bottomright = self.rect.bottomright
        if ori == O_RIGHT or ori == O_DOWN: r.topleft = (0, 0)
        pygame.draw.rect (self.buffer, F_COLOR_FG, r)
        rp = self.buffer.get_rect()
        if ori == O_RIGHT:
            pygame.draw.polygon (self.buffer, F_COLOR_FG, [
                rp.midright, (rp.right-G_SIZE_POINTER, rp.centery-int(G_SIZE_POINTER/2)),
                (rp.right-G_SIZE_POINTER, rp.centery+int(G_SIZE_POINTER/2)), rp.midright
            ], 0)
            pygame.draw.polygon (self.buffer, F_COLOR_BG, [
                (rp.width-4, rp.centery), (rp.right-G_SIZE_POINTER-4, rp.centery-int(G_SIZE_POINTER/2)),
                (rp.right-G_SIZE_POINTER-4, rp.centery+int(G_SIZE_POINTER/2)), (rp.width-4, rp.centery)
            ], 0)
        elif ori == O_LEFT:
            pygame.draw.polygon (self.buffer, F_COLOR_FG, [
                rp.midleft, (rp.left+G_SIZE_POINTER, rp.centery-int(G_SIZE_POINTER/2)),
                (G_SIZE_POINTER, rp.centery+int(G_SIZE_POINTER/2)), rp.midleft
            ], 0)
            pygame.draw.polygon (self.buffer, F_COLOR_BG, [
                (4, rp.centery), (G_SIZE_POINTER+4, rp.centery-int(G_SIZE_POINTER/2)),
                (G_SIZE_POINTER+4, rp.centery+int(G_SIZE_POINTER/2)), (4, rp.centery)
            ], 0)
        elif ori == O_UP:
            pygame.draw.polygon (self.buffer, F_COLOR_FG, [
                rp.midtop, (rp.centerx-int(G_SIZE_POINTER/2), G_SIZE_POINTER),
		(rp.centerx+int(G_SIZE_POINTER/2), G_SIZE_POINTER), rp.midtop
            ], 0)
            pygame.draw.polygon (self.buffer, F_COLOR_BG, [
                (rp.centerx, 4), (rp.centerx-int(G_SIZE_POINTER/2), G_SIZE_POINTER+4),
                (rp.centerx+int(G_SIZE_POINTER/2), G_SIZE_POINTER+4), (rp.centerx, 4)
            ], 0)
        elif ori == O_DOWN:
            pygame.draw.polygon (self.buffer, F_COLOR_FG, [
                rp.midbottom, (rp.centerx-int(G_SIZE_POINTER/2), rp.bottom-G_SIZE_POINTER),
                (rp.centerx+int(G_SIZE_POINTER/2), rp.bottom-G_SIZE_POINTER), rp.midbottom
            ], 0)
            pygame.draw.polygon (self.buffer, F_COLOR_BG, [
                (rp.centerx, rp.bottom-4), (rp.centerx-int(G_SIZE_POINTER/2), rp.bottom-G_SIZE_POINTER-4),
                (rp.centerx+int(G_SIZE_POINTER/2), rp.bottom-G_SIZE_POINTER-4), (rp.centerx, rp.bottom-4)
            ], 0)
        r.size = (r.width-4, r.height - 4)
        r.top += 2
        r.left += 2
        self.display = self.buffer.subsurface(r)
        self.display.fill (F_COLOR_BG)
	
    def set_value (self, string):
        fig = self.text.render (string, True, F_COLOR_FG)
        r = fig.get_rect()
        r.right = self.display.get_rect().w - 4
        self.display.fill (F_COLOR_BG)
        self.display.blit (fig, r)
	
