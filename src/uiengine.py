from typing import List, Dict

"ignore"; from texture import *
"ignore"; from display import *
"ignore"; from hitbox import *

import pygame

class Button(object):
  hover_mod: pygame.Surface
  box: AABBHitbox
  next_menu: str

  def __init__(self, image, hitbox, next_menu):
    typeassert(image, pygame.Surface)
    typeassert(hitbox, AABBHitbox)
    typeassert(next_menu, str)
    self.next_menu = next_menu
    self.box = hitbox
    self.hover_mod = image

class Menu(object):
  button_type: int
  image: pygame.Surface
  buttons: List[Button]

  def __init__(self, image):
    typeassert(image, str)
    self.image = TextureManager.ref().load(image)
    self.buttons = []

  def add_button(self, hover_image, box, next_menu):
    typeassert(hover_image, str)
    typeassert(box, AABBHitbox)
    typeassert(next_menu, str)
    self.buttons.append(Button(TextureManager.ref().load(hover_image), box, next_menu))

class UIEngine(object):
  menus: Dict[str, Menu]
  active: str
  render_target: pygame.Surface
  mousepos: Vec2

  def __init__(self):
    ics_log(LOGLEVEL_INFO, "Initialize UI Engine")
    self.menus = {}
    self.render_target = pygame.display.get_surface()
    self.mousepos = Vec2(0, 0)
    self.active = "start"

  def draw(self):
    menu = self.menus[self.active]
    nimage = menu.image
    for button in menu.buttons:
      aabb = button.box
      if aabb.contains_point(self.mousepos):
        nimage = button.hover_mod
    self.render_target.blit(nimage, pygame.Rect((0, 0), translate_px(Vec2(1920, 1080)).as_tuple()))

  def mousemove(self, pos):
    typeassert(pos, Vec2)
    self.mousepos = pos

  def click(self, pos):
    typeassert(pos, Vec2)
    # TODO