"ignore"; from gameengine import *

# The main function. This will be invoked.
def main():
  init_display()
  eng = GameEngine()
  pl = Player()
  pl.body.center = Vec2(500, 0)
  eng.game.players.append(pl)
  while True:
    eng.view.pollevent()
    eng.tick()
    eng.draw()

if __name__ == "__main__":
  main()