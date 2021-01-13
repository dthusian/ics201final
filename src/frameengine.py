"ignore"; from game import *

class FrameEngine(object):
  game: Game

  def __init__(self, game):
    typeassert(game, Game)
    self.game = game

  def tick(self):
    # Make a list of player collisions
    attacks = []
    for pl in self.game.players:
      # If current frame is attacking...
      if pl.active_seq is not None and pl.active_seq.frames[pl.seq_index].attack > 0:
        for pl2 in self.game.players:
          attack_box = CircleHitbox(pl.body + pl.active_seq.attackbox, pl.active_seq.attackbox.radius)
          if touching(attack_box, pl2.body) and not pl2.active_seq.frames[pl2.seq_index].armor:
            attacks.append((pl2, pl))
    for atk in attacks:
      # Process the player being hit
      target, attack = atk
      cframe = attack.active_seq.frames[attack.seq_index]
      target.damage += cframe.attack
      target.vel += cframe.accel
      target.seq_index = 0
      target.active_seq = None
    for pl in self.game.players:
      if pl.active_seq is not None:
        pl.seq_index += 1
        if len(pl.active_seq.frames) == pl.seq_index:
          pl.seq_index = 0
          pl.active_seq = None