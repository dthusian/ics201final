"ignore"; from physicsengine import *
"ignore"; from frameengine import *
"ignore"; from gameview import *
import pygame
import time

controls_map = {}
controls_map[pygame.K_w] = "player1.jump"
controls_map[pygame.K_a] = "player1.left"
controls_map[pygame.K_d] = "player1.right"
controls_map[pygame.K_1] = "player1.atk"
controls_map[pygame.K_UP] = "player2.jump"
controls_map[pygame.K_LEFT] = "player2.left"
controls_map[pygame.K_RIGHT] = "player2.right"
controls_map[pygame.K_COMMA] = "player2.atk"

# GameEngine holds all the objects and also assists in piping
# input events to the game.
class GameEngine(object):
  game: Game
  view: GameView
  physics: PhysicsEngine
  frames: FrameEngine

  def __init__(self):
    self.game = Game()
    self.view = GameView(self.game)
    self.physics = PhysicsEngine(self.game)
    self.frames = FrameEngine(self.game)

  def mainloop(self):
    while True:
      ev = self.view.pollevent()
      self.handle_event(ev)
      self.tick()
      self.draw()

  def handle_event(self, ev):
    typeassert(ev, pygame.event.EventType)
    if ev.type == pygame.KEYUP:
      mapped = controls_map.get(ev.key)
      if mapped:
        self.physics.release_key(mapped)
    if ev.type == pygame.KEYDOWN:
      mapped = controls_map.get(ev.key)
      if mapped:
        self.physics.press_key(mapped)
        self.frames.press_key(mapped)

  def draw(self):
    self.view.draw()

  def tick(self):
    pressed = pygame.key.get_pressed()
    buttons = controls_map.items()
    controls = {}
    for button in buttons:
      controls[button[1]] = pressed[button[0]]
    self.physics.process_keys(controls)
    self.physics.tick()
    self.frames.tick()

  @staticmethod
  def framerate_thread():
    pass