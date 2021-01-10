"ignore"; from gameview import *
"ignore"; from physics import *

import time

def millis():
  return int(round(time.time() * 1000))

"debug"; mstart = millis()

def main():
  init_display()
  gv = GameView(Game())
  eng = PhysicsEngine(gv.game)
  pl = Player()
  pl.body.center = Vec2(500, 0)
  gv.game.players.append(pl)
  while True:
    gv.pollevent()
    if millis() - mstart > 15000:
      eng.tick()
    gv.draw()

if __name__ == "__main__":
  main()