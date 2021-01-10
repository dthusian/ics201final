import math

"ignore"; from game import *

class PhysicsEngine(object):
  game: Game
  def __init__(self, game):
    typeassert(game, Game)
    self.game = game

  # Takes a player at original position
  def collide(self, player, box):
    typeassert(player, Player)
    typeassert(box, AABBHitbox)
    tmp0 = player.vel * player.vel
    totalv = math.sqrt(tmp0.x + tmp0.y)
    minbound = 0.0
    maxbound = 1.0
    epsilon = 0.001
    while abs(minbound - maxbound) > epsilon:
      mid = (minbound + maxbound) / 2
      newplayer = CircleHitbox(player.body.center + player.vel * Vec2(mid, mid), player.body.radius)
      if touching(newplayer, box):
        maxbound = mid
      else:
        minbound = mid
    realv = minbound
    realvel = Vec2(realv, realv) * player.vel
    player.body.center += realvel
    player.vel = Vec2(0, 0)
  
  def tick(self):
    for pl in self.game.players:
      pl.vel += Vec2(0, 0.02)
    for pl in self.game.players:
      circle = CircleHitbox(pl.body.center, pl.body.radius)
      circle.center += pl.vel
      for box in self.game.mapboxes:
        if touching(circle, box):
          self.collide(pl, box)
          break
      else:
        pl.body.center += pl.vel