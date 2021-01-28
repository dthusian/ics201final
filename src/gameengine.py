"ignore"; from physicsengine import *
"ignore"; from frameengine import *
"ignore"; from gameview import *
"ignore"; from uiengine import *
import pygame

# Maps the controls from pygame keys to key id strings
controls_map = {}
controls_map[pygame.K_w] = "player1.jump"
controls_map[pygame.K_a] = "player1.left"
controls_map[pygame.K_s] = "player1.down"
controls_map[pygame.K_d] = "player1.right"
controls_map[pygame.K_1] = "player1.atk"
controls_map[pygame.K_UP] = "player2.jump"
controls_map[pygame.K_LEFT] = "player2.left"
controls_map[pygame.K_RIGHT] = "player2.right"
controls_map[pygame.K_DOWN] = "player2.down"
controls_map[pygame.K_COMMA] = "player2.atk"

# Menus
startMenu = Menu("menu/start")
startMenu.add_button("menu/start_hover_play", AABBHitbox(Vec2(1129, 365), Vec2(483, 146)), "game")
startMenu.add_button("menu/start_hover_help", AABBHitbox(Vec2(1140, 600), Vec2(483, 146)), "help")
instructionsMenu = Menu("menu/help")
instructionsMenu.add_button("menu/help_hover_back", AABBHitbox(Vec2(125, 65), Vec2(270, 73)), "start")

# GameEngine holds all the objects and also assists in piping
# input events to the game.
# Alert: GameEngine isn't technically an engine.
class GameEngine(object):
  game: Game
  view: GameView
  physics: PhysicsEngine
  frames: FrameEngine
  ui: UIEngine
  clock: pygame.time.Clock
  exit: bool

  def __init__(self):
    ics_log(LOGLEVEL_INFO, "Initialize Game Engine")
    self.game = Game()
    self.view = GameView(self.game)
    self.physics = PhysicsEngine(self.game)
    self.frames = FrameEngine(self.game)
    self.ui = UIEngine()
    self.ui.menus["start"] = startMenu
    self.ui.menus["help"] = instructionsMenu
    self.clock = pygame.time.Clock()
    ics_log(LOGLEVEL_INFO, "Game Engine finished initialization")
    self.exit = False

  # Runs the main loop of the game
  def mainloop(self):
    while True:
      while True:
        ev = self.view.pollevent()
        if ev.type == pygame.NOEVENT:
          break
        self.handle_event(ev)
      if self.exit:
        ics_log(LOGLEVEL_INFO, "Game shutdown")
        break
      self.tick()
      self.draw()
      self.clock.tick(60)

  # Handles input events
  def handle_event(self, ev):
    typeassert(ev, pygame.event.EventType)
    # For Game
    if ev.type == pygame.KEYDOWN:
      mapped = controls_map.get(ev.key)
      if mapped:
        self.physics.press_key(mapped)
        self.frames.press_key(mapped)
    # For processing UI when game isn't active
    if self.ui.active != "game":
      if ev.type == pygame.MOUSEBUTTONUP:
        self.ui.click(Vec2.from_tuple(ev.pos))
      if ev.type == pygame.MOUSEMOTION:
        self.ui.mousemove(Vec2.from_tuple(ev.pos))
    # For ending screen
    if self.game.winner != -1:
      if ev.type == pygame.MOUSEBUTTONDOWN:
        self.exit = True

  # Draw!
  def draw(self):
    if self.game.winner != -1:
      # Ending screen
      _scaled_size = translate_px(Vec2(1920, 1080))
      _scaled_image = pygame.transform.scale(TextureManager.ref().load("stage/gameend"), (int(_scaled_size.x), int(_scaled_size.y)))
      self.view.render_target.blit(_scaled_image, (0, 0))
      pygame.display.flip()
    elif self.ui.active == "game":
      self.view.draw()
    else:
      self.ui.draw()

  # Tick!
  def tick(self):
    # Just go through all the engines and tick them and stuff
    if self.ui.active != "game": return
    pressed = pygame.key.get_pressed()
    buttons = controls_map.items()
    controls = {}
    for button in buttons:
      controls[button[1]] = pressed[button[0]]
    self.frames.process_keys(controls)
    self.frames.tick()
    self.physics.process_keys(controls)
    self.physics.tick()