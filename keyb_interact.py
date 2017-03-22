#!/usr/bin/env python


# Untouched from original implementation

import interact
import snake_game.directions as D

import pygame
import pygame.locals

class KeyBInteract(interact.Interact):
  def PerformAndReturnNextMove(self, sl):
    d = sl.state.direction

    for e in pygame.event.get():
      if e.type is not pygame.locals.KEYDOWN:
        return sl.state.direction

      if e.key == pygame.locals.K_UP:
        d = D.UP
      if e.key == pygame.locals.K_DOWN:
        d = D.DOWN
      if e.key == pygame.locals.K_LEFT:
        d = D.LEFT
      if e.key == pygame.locals.K_RIGHT:
        d = D.RIGHT
    sl.Move(d)
    return d
