"ignore"; from base import *
"ignore"; from hitbox import *
"ignore"; from frames import *

# Represents a player. There's not much here right now.
class Player(object):
  body: CircleHitbox
  active_seq: FrameSequence
  vel: Vec2
  damage: int

  # Constructs a player with default parameters.
  def __init__(self):
    self.body = CircleHitbox(Vec2(-600, -600), 40)
    self.vel = Vec2(0, 0)
    self.damage = 0

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
