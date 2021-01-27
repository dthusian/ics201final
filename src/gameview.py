import pygame

"ignore"; from game import *
"ignore"; from display import *

# The GameView class helps with rendering the game,
# i.e. translating the data structures found in Game class
# to pixels on a screen.
# Most of the code in GameView will work as long as your aspect ratio is 16:9.
# GameView automatically scales if the display isn't 1920x1080.
class GameView(object):
  game: Game
  render_target: pygame.Surface

  # Constructs a GameView with a Game.
  def __init__(self, game):
    ics_log(LOGLEVEL_INFO, "Initialize Game View")
    self.render_target = pygame.display.get_surface()
    self.game = game
  
  # Draws the game to the window.
  def draw(self):
    pygame.draw.rect(self.render_target, (0, 0, 0), pygame.Rect((0, 0), translate_px(Vec2(1920, 1080)).as_tuple()))
    for box in self.game.mapboxes:
      pygame.draw.rect(self.render_target, (0, 0, 255),
        pygame.Rect(
          translate_px((box.center - box.size / Vec2(2, 2))).as_tuple(),
          translate_px(box.size).as_tuple()
        )
      )
    colors = [(255, 0, 0), (0, 255, 0)]
    for pl in self.game.players:
      pygame.draw.circle(self.render_target, colors[len(colors) - 1],
        translate_px(pl.body.center).as_tuple(),
      translate_px(pl.body.radius))
      colors.pop()
    pygame.display.flip()
  
  # Gets a pygame event and returns it.
  def pollevent(self):
    return pygame.event.poll()