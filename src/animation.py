"ignore"; from texture import *
"ignore"; from display import *

import pygame

# Constant for sprite scaling
_sprite_scale = 2.5

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

  def draw(self, render_target, pos):
    typeassert(pos, Vec2)
    typeassert(render_target, pygame.Surface)
    _scaled_size = translate_px(Vec2.from_tuple(self.main_tex.get_size())
                                * Vec2(_sprite_scale, _sprite_scale))
    _scaled_image = pygame.transform.scale(self.main_tex, (int(_scaled_size.x), int(_scaled_size.y)))
    render_target.blit(_scaled_image, translate_px(pos - Vec2.from_tuple(self.main_tex.get_size())).as_tuple())
    pass

# Animation.
class Animation(object):
  frames: [ImageFrame]
  flag: str

  def __init__(self, length):
    self.frames = [ImageFrame() for _ in range(length)]
    self.flag = ""

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
    na.flag = self.flag
    for i in range(len(self.frames)):
      src = self.frames[i]
      dst = na.frames[i]
      dst.main_tex = pygame.transform.flip(src.main_tex.copy(), True, False)
      dst.weapon_tex = pygame.transform.flip(src.weapon_tex.copy(), True, False)
      dst.weapon_rot = 360 - src.weapon_rot
      dst.weapon_pos = mirror_vec2(src.weapon_pos)
    return na

  @staticmethod
  def load_keyframes(path, length, ratio):
    typeassert(path, str)
    typeassert(length, int)
    typeassert(ratio, int)
    ret = Animation(length * ratio)
    for i in range(length):
      for j in range(0, ratio):
        index = i * ratio + j
        ret.frames[index] = ImageFrame()
        ret.frames[index].main_tex = TextureManager.ref().load("{}@{}".format(path, i))
    return ret

  @staticmethod
  def load_single(path):
    typeassert(path, str)
    ret = Animation(1)
    ret.frames[0] = ImageFrame()
    ret.frames[0].main_tex = TextureManager.ref().load(path)
    return ret