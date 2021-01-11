"ignore"; from base import *

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
  "ignore"; from game import *
  pass

class Frame(object):
  gravity: float
  armor: float
  accel: float
  hook: Callable[[Player, int], None]

class FrameSequence(object):
  cancelvel: bool
  frames: [Frame]

  def __init__(self, length):
    typeassert(length, int)
    self.frames = [Frame() for _ in range(length)]
    self.cancelvel = True

  def setrange(self, rang, key, val):
    typeassertmany(rang, [list, range])
    typeassert(rang[0], int)
    typeassert(key, str)
    typeassertmany(val, [float])
    for i in rang:
      setattr(self.frames[i], key, val)

  def addhook(self, hook, frame):
    typeassert(frame, int)
    typeassert(hook, type(lambda: 0))
    self.frames[frame].hook = hook
