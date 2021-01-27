"ignore"; from texture import *
"ignore"; from display import *

import pygame

class Menu(object):
  button_type: int
  image: pygame.Surface

  def __init__(self, image, button_type):
    typeassert(image, str)
    self.image = TextureManager.ref().load(image)
    self.button_type = button_type

class UIEngine(object):
  menus: dict[str, Menu]
  active: str
  render_target: pygame.Surface

  def __init__(self):
    self.menus = {}
    self.render_target = pygame.display.get_surface()

  def draw(self):
    self.render_target.blit(self.menus[self.active].image,
                            pygame.Rect((0, 0), translate_px(Vec2(1920, 1080)).as_tuple()))
  def click(self, location):
    typeassert(location, Vec2)
    # TODO