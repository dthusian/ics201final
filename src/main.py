"ignore"; from gameengine import *

# The main function. This will be invoked.
def main():
  init_display()
  eng = GameEngine()
  pl = Player()
  pl2 = Player()
  pl.body.center = Vec2(500, 0)
  pl2.body.center = Vec2(600, 0)
  eng.game.players.append(pl)
  eng.game.players.append(pl2)
  eng.mainloop()

if __name__ == "__main__":
  main()