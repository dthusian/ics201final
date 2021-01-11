"ignore"; from gameview import *
"ignore"; from physicsengine import *

# The main function. This will be invoked.
def main():
  init_display()
  gv = GameView(Game())
  eng = PhysicsEngine(gv.game)
  pl = Player()
  pl.body.center = Vec2(500, 0)
  gv.game.players.append(pl)
  while True:
    gv.pollevent()
    eng.tick()
    gv.draw()

if __name__ == "__main__":
  main()