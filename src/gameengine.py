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
    controls = {
      "player1.jump": pressed[pygame.K_w],
      "player1.left": pressed[pygame.K_a],
      "player1.right": pressed[pygame.K_d]
    }
    self.physics.process_keys(controls)

    self.physics.tick()
    self.frames.tick()