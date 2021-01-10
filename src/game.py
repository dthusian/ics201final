"ignore"; from base import *
"ignore"; from player import *

# Represents an ongoing game.
class Game(object):
  players: [Player]
  mapboxes: [AABBHitbox]
  def __init__(self):
    # Initialize dummy map
    self.mapboxes = []
    box = AABBHitbox(Vec2(960, 600), Vec2(1200, 100))
    self.mapboxes.append(box)
    self.players = []
