"ignore"; from hitbox import *

from typing import Callable, Union

class Frame(object):
  gravity: float
  armor: float
  attack: float
  vel_other: Vec2
  vel_self: Vec2
  stun: bool
  hook: Union[Callable[[object, int], None], None]

  def __init__(self):
    self.gravity = 1.0
    self.armor = 0.0
    self.attack = 0.0
    self.vel_other = Vec2(0, 0)
    self.vel_self = Vec2(0, 0)
    self.stun = False
    self.hook = None

class FrameSequence(object):
  cancelvel: bool
  attackbox: CircleHitbox
  frames: list[Frame]

  def __init__(self, length):
    typeassert(length, int)
    self.frames = [Frame() for _ in range(length)]
    self.cancelvel = True
    self.attackbox = CircleHitbox(Vec2(0, 0), 40)

  def setrange(self, rang, key, val):
    typeassertmany(rang, [list, range])
    typeassert(rang[0], int)
    typeassert(key, str)
    typeassertmany(val, [float, bool, Vec2, type(None)])
    for i in rang:
      setattr(self.frames[i], key, val)

  def setall(self, key, val):
    typeassert(key, str)
    typeassertmany(val, [float, bool, Vec2, type(None)])
    for frame in self.frames:
      setattr(frame, key, val)

  def addhook(self, hook, frame):
    typeassert(frame, int)
    typeassert(hook, type(lambda: 0))
    self.frames[frame].hook = hook
