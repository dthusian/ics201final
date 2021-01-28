"ignore"; from game import *
"ignore"; from framedef import *

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

  # (Internal method) Triggers a player to move (if it can)
  def try_move(self, keys, pid):
    pl = self.game.players[pid]
    if keys["player{}.left".format(pid + 1)] and pl.is_free():
      pl.movevec = Vec2(-6.5, 0)
      if pl.active_animation.flag != "move":
        pl.set_animation(animMoveStart.mirror_x())
    if keys["player{}.right".format(pid + 1)] and pl.is_free():
      pl.movevec = Vec2(6.5, 0)
      if pl.active_animation.flag != "move":
        pl.set_animation(animMoveStart)

  # (Internal method) Triggers a player to jump if it can
  def try_jump(self, key, pid):
    pl = self.game.players[pid]
    if key == "player{}.jump".format(pid + 1) and pl.jumps and pl.is_free():
      pl.jumps -= 1
      pl.vel = Vec2(0, -16)
      pl.set_animation(animJumpStart)

  # Engine methods

  def process_keys(self, keys):
    typeassert(keys, dict)
    self.game.players[0].movevec = Vec2(0, 0)
    self.game.players[1].movevec = Vec2(0, 0)
    self.try_move(keys, 0)
    self.try_move(keys, 1)

  def press_key(self, key):
    self.try_jump(key, 0)
    self.try_jump(key, 1)

  def tick(self):
    G = 0.7
    playing_area = AABBHitbox(Vec2(1920 / 2, 1080 / 2), Vec2(1920 + 400, 1080 + 250))
    for pl in self.game.players:
      if pl.active_seq is None:
        pl.vel += Vec2(0, G)
      else:
        pl.vel += Vec2(0, G * pl.active_seq.frames[pl.seq_index].gravity)
    for pl in self.game.players:
      # Handling of jumps
      # Players only get 2 jumps
      prioryvel = pl.vel.y
      collided = self.safemove(pl, pl.movevec)
      if collided and prioryvel > 0:
        pl.jumps = 2
      collided = self.safemove(pl, pl.vel)
      if collided and prioryvel > 0:
        pl.jumps = 2
      if not playing_area.contains_point(pl.body.center):
        self.game.winner = not self.game.players.index(pl)
