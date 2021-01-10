"ignore"; from hitbox import *

class Player(object):
  body: CircleHitbox
  vel: Vec2
  damage: int
  def __init__(self):
    self.body = CircleHitbox(Vec2(-600, -600), 40)
    self.vel = Vec2(0, 0)
    self.damage = 0