"ignore"; from game import *
"ignore"; from framedef import *
from typing import Dict

class FrameEngine(object):
  game: Game
  keys: Dict[str, bool]
  _debug_frameindex: int

  def __init__(self, game):
    typeassert(game, Game)
    self.game = game
    self._debug_frameindex = 0

  def try_atk(self, pindex):
    pl = self.game.players[pindex]
    if not pl.active_seq or pl.active_seq.frames[pl.seq_index].stun:
      pl.active_seq = playerUpB # Do something here
      pl.seq_index = 0

  def process_keys(self, keys):
    self.keys = keys

  def press_key(self, key):
    if key == "player1.atk":
      self.try_atk(0)
    if key == "player2.atk":
      self.try_atk(1)

  def tick(self):
    self._debug_frameindex += 1
    # Make a list of player collisions
    attacks = []
    for pl in self.game.players:
      if pl.stun_frames > 0: pl.stun_frames -= 1
      # If current frame is attacking...
      if pl.active_seq:
        pl.vel = pl.active_seq.frames[pl.seq_index].vel_self
        if pl.active_seq.frames[pl.seq_index].attack > 0:
          print("FrameEngine.tick i={} pl={} seq={}".format(self._debug_frameindex, self.game.players.index(pl), pl.seq_index))
          # Check which players are touching
          for pl2 in self.game.players:
            if pl2 != pl and pl2.stun_frames == 0:
              attack_box = CircleHitbox(pl.body.center + pl.active_seq.attackbox.center, pl.active_seq.attackbox.radius)
              if touching(attack_box, pl2.body):
                attacks.append((pl2, pl))
    for atk in attacks:
      # Process the player being hit
      target, attack = atk
      cframe = attack.active_seq.frames[attack.seq_index]
      target.damage += cframe.attack
      target.vel += cframe.vel_other
      target.seq_index = 0
      target.active_seq = None
      target.stun_frames = attack.active_seq.stun_frames
    for pl in self.game.players:
      if pl.active_seq:
        pl.seq_index += 1
        if len(pl.active_seq.frames) == pl.seq_index:
          pl.seq_index = 0
          pl.active_seq = None