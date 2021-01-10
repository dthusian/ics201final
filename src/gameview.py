import pygame

"ignore"; from game import *

display_size = (1920, 1080)

# Initializes the display subsystem.
# This will also sanity-check the output aspect ratio.
def init_display():
  global display_size
  ics_log(LOGLEVEL_INFO, "Initialize display subsystem")
  pygame.display.init()
  pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  driver = pygame.display.get_driver()
  ics_log(LOGLEVEL_INFO, "Used display driver: %s" % driver)
  # Check the display ratio to ensure it's 16:9
  dispinfo = pygame.display.Info()
  # Assume the display is 1920x1080 if no size detected.
  if dispinfo.current_h <= 0 or dispinfo.current_w <= 0:
    ics_log(LOGLEVEL_WARNING, "Couldn't detect your display size. Assuming 1920x1080.")
  else:
    display_size = (dispinfo.current_w, dispinfo.current_h)
  ratio = dispinfo.current_w / dispinfo.current_h
  expected_ratio = 16 / 9
  if abs(ratio - expected_ratio) > 0.00001:
    # Print warning if ratio isn't 16:9
    ics_log(LOGLEVEL_WARNING, "Display isn't 16:9. The game might look stretched.")

# The GameView class helps with rendering the game,
# i.e. translating the data structures found in Game class
# to pixels on a screen.
# Most of the code in GameView will work as long as your aspect ratio is 16:9.
# GameView automatically scales if the display isn't 1920x1080.
class GameView(object):
  game: Game
  render_target: pygame.Surface
  assumed_size: Vec2

  # Constructs a GameView with a Game.
  def __init__(self, game):
    self.render_target = pygame.display.get_surface()
    self.game = game
    self.assumed_size = Vec2(1920, 1080)
  
  # The scaling logic: translate_px translates coordiantes from a 1920x1080
  # screen to the coordinates of the actual screen. Make sure you call
  # init_display() first to make sure the output ratio is recorded.
  def translate_px(self, v):
    typeassertmany(v, [Vec2, float])
    if typeeq(v, Vec2):
      return Vec2.from_tuple(display_size) * v / self.assumed_size
    if typeeq(v, float):
      return display_size[0] * v / self.assumed_size.x
  
  # untranslate_px is just as important as the translating logic.
  # It's used to translate mouse input coordinates from the real display
  # size to the assumed 1920x1080.
  def untranslate_px(self, v):
    typeassertmany(v, [Vec2])
    if typeeq(v, Vec2):
      return self.assumed_size * v / Vec2.from_tuple(display_size)
  
  # Draws the game to the window.
  def draw(self):
    pygame.draw.rect(self.render_target, (0, 0, 0), pygame.Rect((0, 0), self.translate_px(Vec2(1920, 1080)).as_tuple()))
    for box in self.game.mapboxes:
      pygame.draw.rect(self.render_target, (0, 0, 255),
        pygame.Rect(
          self.translate_px((box.center - box.size / Vec2(2, 2))).as_tuple(),
          self.translate_px(box.size).as_tuple()
        )
      )
    for pl in self.game.players:
      pygame.draw.circle(self.render_target, (255, 0, 0),
        self.translate_px(pl.body.center).as_tuple(),
      self.translate_px(pl.body.radius))
    pygame.display.flip()
  
  # Gets a pygame event and returns it.
  def pollevent(self):
    return pygame.event.poll()