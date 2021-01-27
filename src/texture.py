"ignore"; from base import *

import pygame

from typing import Dict

class TextureManager(object):
  cache: Dict[str, pygame.Surface]

  def __init__(self):
    self.cache = {}

  def load(self, id):
    typeassert(id, str)
    if id in self.cache.keys():
      return self.cache[id]
    else:
      tex = pygame.image.load("./assets/texture/{}.png".format(id))
      self.cache[id] = tex
      return tex

  @staticmethod
  def ref():
    global _instance
    return _instance

_instance = TextureManager()