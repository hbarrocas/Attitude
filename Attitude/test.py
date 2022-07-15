import pygame, sys
from Attitude.pfd import PFD

value = {
        "ASI": 0,
        "ALT": 0,
        "ALTBUG": 0,
        "HDGBUG": 0,
        "BARO": 1013,
        "GS": 0,
        "VSI": 0,
        "ATT": {"bank": 0, "pitch": 0},
        "HDG": 270,
        "SSI": 0
}

def action_inc ():
    global value
    value["ALTBUG"] += 10

def action_dec ():
    global value
    value["ALTBUG"] -= 10

def action_left ():
    global value
    value["ATT"]["bank"] -= 2
    value["HDG"] -= 2
    value["SSI"] -= 0.05

def action_right ():
    global value
    value["ATT"]["bank"] += 2
    value["HDG"] += 2
    value["SSI"] += 0.05

def action_up ():
    global value
    value["ASI"] += 1
    value["GS"] += 1
    value["ALT"] += 5
    value["ATT"]["pitch"] -= 1
    value["VSI"] += 0.2

def action_down ():
    global value
    value["ASI"] -= 1
    value["GS"] -= 1
    value["ALT"] -= 5
    value["ATT"]["pitch"] += 1
    value["VSI"] -= 0.2

def exit ():
    pygame.quit()
    sys.exit(0)

# Setup key bindings
keymap = {
        pygame.K_PERIOD: action_inc,
        pygame.K_COMMA: action_dec,
        pygame.K_UP: action_up,
        pygame.K_DOWN: action_down,
        pygame.K_LEFT: action_left,
        pygame.K_RIGHT: action_right,
        pygame.K_ESCAPE: exit
}

def run ():		
    global value
    global keymap

    pygame.init ()
    display = pygame.display.set_mode((800, 800))		
    pfd = PFD(display, display.get_rect())

    while 1:
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key in keymap: keymap[event.key]()
            pygame.event.clear()

        pfd.set_value (value)
        pfd.render()
        pygame.display.flip()
