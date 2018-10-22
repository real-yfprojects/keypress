#!/usr/bin/env python
# Play sounds on keypresses in Linux
# Originally by Sayan "Riju" Chakrabarti (sayanriju)
# http://rants.sayanriju.co.cc/script-to-make-tick-tick-sound-on-keypres

from Xlib.display import Display
import threading
import os
import time


def zero_key():
    return [0 for i in range(0, 32)]


IGNORED_KEYS = {
    'ZERO': zero_key(),
}

IGNORED_KEYS['SHIFT'] = list(zero_key())
IGNORED_KEYS['SHIFT'][6] = 4

IGNORED_KEYS['CTL'] = list(zero_key())
IGNORED_KEYS['CTL'][4] = 32

IGNORED_KEYS['ALT'] = list(zero_key())
IGNORED_KEYS['ALT'][8] = 1


class KeyPress(threading.Thread):
    def run(self):
        os.system('aplay sounds/key01.wav')


def main():
    display = Display()
    while True:
        keymap = display.query_keymap()
        if keymap not in IGNORED_KEYS.values():
            KeyPress().start()
            time.sleep(0.08)


if __name__ == '__main__':
    main()
