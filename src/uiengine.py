from typing import List, Dict

"ignore"; from texture import *
"ignore"; from display import *
"ignore"; from hitbox import *

import pygame

# Represents a button.
# This is an object that can be clicked
# and will go to another menu or the game
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

# Represents a menu. This is an image with buttons on it.
class Menu(object):
  button_type: int
  image: pygame.Surface
  buttons: List[Button]

  def __init__(self, image):
    typeassert(image, str)
    self.image = TextureManager.ref().load(image)
    self.buttons = []

  # Adds a button to the menu.
  def add_button(self, hover_image, box, next_menu):
    typeassert(hover_image, str)
    typeassert(box, AABBHitbox)
    typeassert(next_menu, str)
    self.buttons.append(Button(TextureManager.ref().load(hover_image), box, next_menu))

# This engine processes UI and clicking
# and changing menus
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

  # All of these are engine methods

  def draw(self):
    menu = self.menus[self.active]
    nimage = menu.image
    # Look for if a button is being hovered
    for button in menu.buttons:
      aabb = button.box
      if aabb.contains_point(self.mousepos):
        nimage = button.hover_mod
    size = translate_px(Vec2(1920, 1080))
    scaled_image = pygame.transform.scale(nimage, (int(size.x), int(size.y)))
    self.render_target.blit(scaled_image, (0, 0))
    pygame.display.flip()

  def mousemove(self, pos):
    typeassert(pos, Vec2)
    self.mousepos = pos

  def click(self, pos):
    typeassert(pos, Vec2)
    menu = self.menus[self.active]
    for button in menu.buttons:
      aabb = button.box
      if aabb.contains_point(pos):
        self.active = button.next_menu