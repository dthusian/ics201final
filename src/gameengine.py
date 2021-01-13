"ignore"; from physicsengine import *
"ignore"; from frameengine import *
"ignore"; from gameview import *

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

  def draw(self):
    self.view.draw()

  def tick(self):
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w] and self.game.players[0].jumps:
      self.game.players[0].jumps -= 1
      self.game.players[0].vel += Vec2(0, -0.5)
    if pressed[pygame.K_a]:
      self.game.players[0]

    self.physics.tick()
    self.frames.tick()