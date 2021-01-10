"ignore"; from hitbox import *

# Represents a player. There's not much here right now.
class Player(object):
  body: CircleHitbox
  vel: Vec2
  damage: int

  # Constructs a player with default parameters.
  def __init__(self):
    self.body = CircleHitbox(Vec2(-600, -600), 40)
    self.vel = Vec2(0, 0)
    self.damage = 0