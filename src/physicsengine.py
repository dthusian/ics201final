"ignore"; from game import *

# The physics engine. It processes physics objects (like players) moving
class PhysicsEngine(object):
  game: Game

  def __init__(self, game):
    typeassert(game, Game)
    ics_log(LOGLEVEL_INFO, "Initialize Physics Engine")
    self.game = game

  # Moves a player along it's velocity, checking for obstructions.
  # This function uses a binary search, so it's not the most efficient,
  # but it's definitely the simplest.
  def collide(self, player, box):
    typeassert(player, Player)
    typeassert(box, AABBHitbox)
    # Classical binary search variables
    minbound = 0.0
    maxbound = 1.0
    epsilon = 0.001 # Tolerance
    while abs(minbound - maxbound) > epsilon:
      # Check the midpoint for collision
      mid = (minbound + maxbound) / 2
      newplayer = CircleHitbox(player.body.center + player.vel * Vec2(mid, mid), player.body.radius)
      # Move bounds accordingly
      if touching(newplayer, box):
        maxbound = mid
      else:
        minbound = mid
    # Now that we know where the player can go, move them there
    realv = minbound - 0.01
    realvel = Vec2(realv, realv) * player.vel
    player.body.center += realvel
    player.vel = Vec2(0, 0)

  # Move a player with collision checks.
  def safemove(self, pl, vec):
    circle = CircleHitbox(pl.body.center, pl.body.radius)
    circle.center += vec
    for box in self.game.mapboxes:
      if touching(circle, box):
        self.collide(pl, box)
        return True
    else:
      pl.body.center += vec
      return False

  # Engine methods

  def process_keys(self, keys):
    typeassert(keys, dict)
    self.game.players[0].movevec = Vec2(0, 0)
    self.game.players[1].movevec = Vec2(0, 0)
    if keys["player1.left"] and self.game.players[0].active_seq is None:
      self.game.players[0].movevec = Vec2(-6.5, 0)
    if keys["player1.right"] and self.game.players[0].active_seq is None:
      self.game.players[0].movevec = Vec2(6.5, 0)
    if keys["player2.left"] and self.game.players[1].active_seq is None:
      self.game.players[1].movevec = Vec2(-6.5, 0)
    if keys["player2.right"] and self.game.players[1].active_seq is None:
      self.game.players[1].movevec = Vec2(6.5, 0)

  def press_key(self, key):
    if key == "player1.jump" and self.game.players[0].jumps and self.game.players[0].active_seq is None:
      self.game.players[0].jumps -= 1
      self.game.players[0].vel = Vec2(0, -16)
    if key == "player2.jump" and self.game.players[1].jumps and self.game.players[1].active_seq is None:
      self.game.players[1].jumps -= 1
      self.game.players[1].vel = Vec2(0, -16)
    
  def tick(self):
    G = 0.7
    for pl in self.game.players:
      if pl.active_seq is None:
        pl.vel += Vec2(0, G)
      else:
        pl.vel += Vec2(0, G * pl.active_seq.frames[pl.seq_index].gravity)
    for pl in self.game.players:
      prioryvel = pl.vel.y
      collided = self.safemove(pl, pl.movevec)
      if collided and prioryvel > 0:
        pl.jumps = 2
      collided = self.safemove(pl, pl.vel)
      if collided and prioryvel > 0:
        pl.jumps = 2