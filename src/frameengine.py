"ignore"; from game import *

class FrameEngine(object):
  game: Game

  def __init__(self, game):
    typeassert(game, Game)
    self.game = game

  def tick(self):
    pass