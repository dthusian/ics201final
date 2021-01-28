import pygame

"ignore"; from base import *

# Display size
# I am emotionally unable to write a non-DPI-aware application
# (technically this isn't DPI-aware because it doesn't know the screen dimensions but just go with it)
display_size = (1920, 1080)
assumed_size = Vec2(1920, 1080)

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
  # Check the ratio
  ratio = dispinfo.current_w / dispinfo.current_h
  expected_ratio = 16 / 9
  if abs(ratio - expected_ratio) > 0.00001:
    # Print warning if ratio isn't 16:9
    ics_log(LOGLEVEL_WARNING, "Display isn't 16:9. The game might look stretched.")

# The scaling logic: translate_px translates coordiantes from a 1920x1080
# screen to the coordinates of the actual screen. Make sure you call
# init_display() first to make sure the output ratio is recorded.
def translate_px(v):
  typeassertmany(v, [Vec2, float])
  if typeeq(v, Vec2):
    return Vec2.from_tuple(display_size) * v / assumed_size
  if typeeq(v, float):
    return display_size[0] * v / assumed_size.x

# untranslate_px is just as important as the translating logic.
# It's used to translate mouse input coordinates from the real display
# size to the assumed 1920x1080.
def untranslate_px(v):
  typeassertmany(v, [Vec2])
  if typeeq(v, Vec2):
    return assumed_size * v / Vec2.from_tuple(display_size)