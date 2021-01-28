"ignore"; from texture import *

import pygame

# Represents one frame of an image
class ImageFrame(object):
  main_tex: pygame.Surface
  weapon_tex: pygame.Surface
  weapon_pos: Vec2
  weapon_rot: float

  def __init__(self):
    self.main_tex = pygame.Surface((0, 0), 0)
    self.weapon_tex = pygame.Surface((0, 0), 0)
    self.weapon_pos = Vec2(0, 0)
    self.weapon_rot = 0

# Animation. Surprisingly simple class
class Animation(object):
  frames: [ImageFrame]

  def __init__(self, length):
    self.frames = [ImageFrame() for _ in range(length)]

  def setrange(self, rang, key, val):
    typeassertmany(rang, [list, range])
    typeassert(rang[0], int)
    typeassert(key, str)
    for i in rang:
      setattr(self.frames[i], key, val)

  def setall(self, key, val):
    typeassert(key, str)
    for frame in self.frames:
      setattr(frame, key, val)

  def mirror_x(self):
    def mirror_vec2(x):
      typeassert(x, Vec2)
      return Vec2(-x.x, x.y)
    na = Animation(len(self.frames))
    for i in range(len(self.frames)):
      src = self.frames[i]
      dst = na.frames[i]
      dst.main_tex = pygame.transform.flip(src.main_tex.copy(), True, False)
      dst.weapon_tex = pygame.transform.flip(src.weapon_tex.copy(), True, False)
      dst.weapon_rot = 360 - src.weapon_rot
      dst.weapon_pos = mirror_vec2(src.weapon_pos)

  @staticmethod
  def load_keyframes(path, length):
    ret = Animation(length)
    for i in range(length):
      ret.frames[i] = ImageFrame()
      ret.frames[i].main_tex = TextureManager.ref().load("{}@{}".format(path, i))
    return ret

  @staticmethod
  def load_single(path):
    ret = Animation(1)
    ret.frames[0] = ImageFrame()
    ret.frames[0].main_tex = TextureManager.ref().load(path)
    return ret