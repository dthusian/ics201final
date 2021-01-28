"ignore"; from frames import *
"ignore"; from animation import *
from typing import Union

# Represents a player. There's not much here right now.
class Player(object):
  body: CircleHitbox

  active_seq: FrameSequence
  seq_index: int
  active_animation: Union[Animation, None]
  animation_index: int

  vel: Vec2
  movevec: Vec2

  stun_frames: int
  damage: int
  jumps: int

  # Constructs a player with default parameters.
  def __init__(self):
    self.body = CircleHitbox(Vec2(-600, -600), 40)
    self.vel = Vec2(0, 0)
    self.damage = 0
    self.active_seq = None
    self.seq_index = 0
    self.jumps = 2
    self.movevec = Vec2(0, 0)
    self.stun_frames = 0
    self.active_animation = Animation.load_keyframes("player/idle", 4)
    self.animation_index = 0

  def set_animation(self, animation):
    typeassert(animation, Animation)
    self.animation_index = 0
    self.active_animation = animation

# Represents an ongoing game.
class Game(object):
  players: list[Player]
  mapboxes: list[AABBHitbox]
  def __init__(self):
    # Initialize dummy map
    self.mapboxes = []
    box = AABBHitbox(Vec2(960, 600), Vec2(1200, 100))
    self.mapboxes.append(box)
    self.players = []
