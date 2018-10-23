#!/usr/bin/env python2

# Plays a sound after a key is pressed
# Adapted from http://stackoverflow.com/questions/22367358/
# Requires python-xlib


import argparse
import os
import threading

from Xlib.display import Display
from Xlib import X, XK
from Xlib.ext import record
from Xlib.protocol import rq


class KeyPress(threading.Thread):

    def run(self):
        os.system('aplay -q sounds/key01.wav')


class Listener:

    ignored_keys = {
        65307: 'ESC',
        65360: 'HOME',
        65361: 'ARROW_LEFT',
        65362: 'ARROW_UP',
        65363: 'ARROW_RIGHT',
        65505: 'L_SHIFT',
        65506: 'R_SHIFT',
        65507: 'L_CTRL',
        65508: 'R_CTRL',
        65513: 'L_ALT',
        65514: 'R_ALT',
        65515: 'SUPER_KEY',
        65288: 'BACKSPACE',
        65364: 'ARROW_DOWN',
        65365: 'PG_UP',
        65366: 'PG_DOWN',
        65367: 'END',
        65377: 'PRTSCRN',
        65535: 'DELETE',
        65383: 'PRINT',
        65509: 'CAPS_LOCK',
        65289: 'TAB',
        65470: 'F1',
        65471: 'F2',
        65472: 'F3',
        65473: 'F4',
        65474: 'F5',
        65475: 'F6',
        65476: 'F7',
        65477: 'F8',
        65478: 'F9',
        65479: 'F10',
        65480: 'F11',
        65481: 'F12',
        65027: 'ALT_GR',
        65379: 'INSERT',
        65300: 'SCROLL_LOCK',
        65299: 'PAUSE',
    }

    def __init__(self, logging=False):
        self.disp = None
        self.logging = logging

    def log(self, message):
        if self.logging:
            print(message)

    def keycode_to_key(self, keycode, state):
        i = 1 if state & X.ShiftMask else 0
        if state & X.Mod1Mask:
            i += 2
        return self.disp.keycode_to_keysym(keycode, i)

    def key_to_string(self, key):
        keys = []
        for name in dir(XK):
            if name.startswith("XK_") and getattr(XK, name) == key:
                keys.append("[%s - %s]" % (key, name))
        if keys:
            return " or ".join(keys)
        return "[%d]" % key

    def down(self, key):
        self.play_sound(key)
        self.print_key(self.key_to_string(key))

    def play_sound(self, key):
        if int(key) not in self.ignored_keys.keys():
            KeyPress().start()

    def print_key(self, key_string):
        self.log("Currently pressed: %s" % key_string)

    def event_handler(self, reply):
        data = reply.data
        while data:
            event, data = rq.EventField(None).parse_binary_value(data, self.disp.display, None, None)
            if event.type == X.KeyPress:
                self.down(self.keycode_to_key(event.detail, event.state))

    def run(self):
        self.disp = Display()
        XK.load_keysym_group('xf86')
        root = self.disp.screen().root
        ctx = self.disp.record_create_context(
            0,
            [record.AllClients],
            [
                {
                    'core_requests': (0, 0),
                    'core_replies': (0, 0),
                    'ext_requests': (0, 0, 0, 0),
                    'ext_replies': (0, 0, 0, 0),
                    'delivered_events': (0, 0),
                    'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
                    'errors': (0, 0),
                    'client_started': False,
                    'client_died': False,
                },
            ])
        self.disp.record_enable_context(ctx, lambda reply: self.event_handler(reply))
        self.disp.record_free_context(ctx)

        while True:
            root.display.next_event()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    Listener(logging=args.verbose).run()
