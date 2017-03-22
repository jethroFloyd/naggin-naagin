#!/usr/bin/env python

# Untouched from original implementation.

import pygame

def MainLoop(interact, artist, new_sl_function, delay=100):
  """ Takes an interact object, artist object, and a function that returns a
  new snake logic and runs the GUI main loop. The delay is also a parameter."""
  sl = new_sl_function()
  while True:
    artist.Draw(sl)
    interact.PerformAndReturnNextMove(sl)
    pygame.time.wait(delay)
    if not sl.IsAlive():
      artist.Draw(sl)
      sl = new_sl_function()
      pygame.time.wait(9*delay)
