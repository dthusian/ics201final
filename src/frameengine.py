"ignore"; from game import *
"ignore"; from framedef import *
from typing import Dict

attackMap = {
  "up": playerUpB,
  "down": playerDownB,
  "left": playerSideB,
  "right": playerSideB.mirror_x(),
  "neutral": None # TODO
}

class FrameEngine(object):
  game: Game
  keys: Dict[str, bool]
  _debug_frameindex: int

  def __init__(self, game):
    typeassert(game, Game)
    ics_log(LOGLEVEL_INFO, "Initialize Frame Engine")
    self.game = game
    self._debug_frameindex = 0

  def try_atk(self, pindex, type_attack):
    pl = self.game.players[pindex]
    if not pl.active_seq or pl.active_seq.frames[pl.seq_index].stun_self:
      if type_attack in attackMap.keys() and attackMap[type_attack] is not None:
        pl.active_seq = attackMap[type_attack]
        pl.seq_index = 0

  def process_keys(self, keys):
    self.keys = keys

  def find_directional_input(self, pid):
    prefix = "player" + str(pid + 1) + "."
    my_keys = [key for key in self.keys.keys() if key.startswith(prefix)]
    for key in my_keys:
      if self.keys[key]:
        return key.removeprefix(prefix)
    return "neutral"

  def press_key(self, key):
    if key == "player1.atk":
      self.try_atk(0, self.find_directional_input(0))
    if key == "player2.atk":
      self.try_atk(1, self.find_directional_input(1))

  # This function will process all the attacks and stuff
  def tick(self):
    self._debug_frameindex += 1
    # Make a list of player collisions
    attacks = []
    for pl in self.game.players:
      # Process stun frames
      if pl.stun_frames > 0: pl.stun_frames -= 1
      # If current frame is attacking...
      if pl.active_seq:
        # Accelerate the player by the amount specified
        pl.vel = pl.active_seq.frames[pl.seq_index].vel_self
        print(pl.vel)
        # Now check for attacks only if frame is attacking
        if pl.active_seq.frames[pl.seq_index].attack > 0:
          # Check which players are touching
          for pl2 in self.game.players:
            # Ignore players who have their stun frames on
            if pl2 != pl and pl2.stun_frames == 0:
              # Ignore players if they are blocking (frame has armor attribute > 0.5)
              if pl2.active_seq is None or pl2.active_seq.frames[pl2.seq_index].armor > 0.5:
                # If all conditions are passed, then add check if the players are touching
                attack_box = CircleHitbox(pl.body.center + pl.active_seq.attackbox.center, pl.active_seq.attackbox.radius)
                if touching(attack_box, pl2.body):
                  # This attack should be handled. Add it to the list.
                  attacks.append((pl2, pl))
    for atk in attacks:
      # Process the player being hit
      target, attack = atk
      cframe = attack.active_seq.frames[attack.seq_index]
      if target.active_seq is not None:
        target.damage += cframe.attack * (1 - target.active_seq.frames[target.seq_index].armor)
      else:
        target.damage += cframe.attack
      target.vel += cframe.vel_other
      target.seq_index = 0
      target.active_seq = None
      target.stun_frames = cframe.stun_other
    for pl in self.game.players:
      if pl.active_seq:
        pl.seq_index += 1
        if len(pl.active_seq.frames) == pl.seq_index:
          pl.seq_index = 0
          pl.active_seq = None