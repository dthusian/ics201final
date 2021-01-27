"ignore"; from base import *

import pygame

from typing import Dict

# Manages and caches textures. Use
# ref() to get an instance for use.
class TextureManager(object):
  cache: Dict[str, pygame.Surface]

  def __init__(self):
    self.cache = {}

  # Loads a texture. If the texture is in cache, use that instead
  def load(self, id):
    typeassert(id, str)
    if id in self.cache.keys():
      return self.cache[id]
    else:
      tex = pygame.image.load("./assets/texture/{}.png".format(id))
      self.cache[id] = tex
      return tex

  # Returns the global instance of the texture manager
  @staticmethod
  def ref():
    global _instance
    return _instance

_instance = TextureManager()