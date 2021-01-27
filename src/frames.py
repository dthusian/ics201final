"ignore"; from hitbox import *

from typing import Callable, Union

# Represents a single Attack Frame
class Frame(object):
  # The multiplier applied to gravity during the frame
  # Lower = less gravity, 0.0 = No gravity, 1.0 = Normal gravity
  gravity: float

  # The amount that damage is reduced
  # Higher = less damage taken, 0.0 = No reduction, 1.0 = Full reduction
  # Alert: armor > 0.5 is considered "super armor" and will prevent the player from being stun
  armor: float

  # The amount of damage dealt.
  attack: float

  # The velocity that a target player will be accelerated by.
  vel_other: Vec2

  # The velocity that self will be accelerated by.
  vel_self: Vec2

  # Whether the player is able to cancel the sequence.
  stun_self: bool

  # How many stun frames target players recieve
  stun_other: int

  # A function that is executed during this frame
  hook: Union[Callable[[object, int], None], None]

  def __init__(self):
    self.gravity = 1.0
    self.armor = 0.0
    self.attack = 0.0
    self.vel_other = Vec2(0, 0)
    self.vel_self = Vec2(0, 0)
    self.stun_self = False
    self.stun_other = 30
    self.hook = None

# FrameSequence
class FrameSequence(object):
  cancelvel: bool
  attackbox: CircleHitbox
  frames: list[Frame]

  def __init__(self, length):
    typeassert(length, int)
    self.frames = [Frame() for _ in range(length)]
    self.cancelvel = True
    self.attackbox = CircleHitbox(Vec2(0, 0), 40)

  # Sets a attribute for a range of frames
  def setrange(self, rang, key, val):
    typeassertmany(rang, [list, range])
    typeassert(rang[0], int)
    typeassert(key, str)
    for i in rang:
      setattr(self.frames[i], key, val)

  # Sets a attribute for all frames
  def setall(self, key, val):
    typeassert(key, str)
    for frame in self.frames:
      setattr(frame, key, val)

  # Adds a hook function to be called on a specific frame
  def addhook(self, hook, frame):
    typeassert(frame, int)
    typeassert(hook, type(lambda: 0))
    self.frames[frame].hook = hook

  # Mirrors the FrameSequence in the x-direction
  # Used for making separate left and right animations
  def mirror_x(self):
    def mirror_vec2(x):
      typeassert(x, Vec2)
      return Vec2(-x.x, x.y)
    def copy_attr(attr, a, b):
      setattr(b, attr, getattr(a, attr))
    fs = FrameSequence(len(self.frames))
    fs.cancelvel = self.cancelvel
    fs.attackbox = CircleHitbox(mirror_vec2(self.attackbox.center), self.attackbox.radius)
    fs.frames = [Frame() for _ in self.frames]
    for i in range(len(self.frames)):
      src = self.frames[i]
      dst = fs.frames[i]
      copy_attr("attack", src, dst)
      dst.vel_self = mirror_vec2(src.vel_self)
      dst.vel_other = mirror_vec2(src.vel_other)
      copy_attr("gravity", src, dst)
      copy_attr("armor", src, dst)
      copy_attr("stun_self", src, dst)
      copy_attr("stun_other", src, dst)
      copy_attr("hook", src, dst)
    return fs