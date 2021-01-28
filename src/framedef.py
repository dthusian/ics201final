"ignore"; from frames import *
"ignore"; from animation import *

# Here we define all the player's moves.
# And all the animations.

playerUpB = FrameSequence(16)

playerUpB.setall("attack", 10.0)
playerUpB.setall("vel_self", Vec2(0, -20))
playerUpB.setall("vel_other", Vec2(0, -9))
playerUpB.setall("gravity", 0.0)
playerUpB.setall("armor", 0.0)
playerUpB.setall("stun_self", True)
playerUpB.setall("stun_other", 40)
playerUpB.frames[15].vel_self = Vec2(0, -10)

playerSideB = FrameSequence(130)
_startlag = range(0, 40)
_active = range(40, 90)
_endlag = range(90, 130)

playerSideB.setrange(_startlag, "attack", 0.0)
playerSideB.setrange(_startlag, "vel_self", Vec2(0, 0))
playerSideB.setrange(_startlag, "vel_other", Vec2(0, 0))
playerSideB.setrange(_startlag, "gravity", 0.0)
playerSideB.setrange(_startlag, "armor", 0.0)
playerSideB.setrange(_startlag, "stun_self", True)
playerSideB.setrange(_startlag, "stun_other", 0)

playerSideB.setrange(_active, "attack", 25.0)
playerSideB.setrange(_active, "vel_self", Vec2(-8, -0.1 ))
playerSideB.setrange(_active, "vel_other", Vec2(-25, 0))
playerSideB.setrange(_active, "gravity", 0.5)
playerSideB.setrange(_active, "armor", 0.8)
playerSideB.setrange(_active, "stun_self", True)
playerSideB.setrange(_active, "stun_other", 125)

playerSideB.setrange(_endlag, "attack", 0.0)
playerSideB.setrange(_endlag, "vel_self", Vec2(-2, 0))
playerSideB.setrange(_endlag, "vel_other", Vec2(0, 0))
playerSideB.setrange(_endlag, "gravity", 1.0)
playerSideB.setrange(_endlag, "armor", 0.0)
playerSideB.setrange(_endlag, "stun_self", True)
playerSideB.setrange(_endlag, "stun_other", 0)

playerDownB = FrameSequence(25)
_startlag = range(0, 3)
_active = range(3, 20)
_endlag = range(20, 25)

playerDownB.setrange(_startlag, "attack", 0.0)
playerDownB.setrange(_startlag, "vel_self", Vec2(0, 0))
playerDownB.setrange(_startlag, "vel_other", Vec2(0, 0))
playerDownB.setrange(_startlag, "gravity", 1.0)
playerDownB.setrange(_startlag, "armor", 0.0)
playerDownB.setrange(_startlag, "stun_self", True)
playerDownB.setrange(_startlag, "stun_other", 0)

playerDownB.setrange(_active, "attack", 0.0)
playerDownB.setrange(_active, "vel_self", Vec2(0, 0))
playerDownB.setrange(_active, "vel_other", Vec2(0, 0))
playerDownB.setrange(_active, "gravity", 0.0)
playerDownB.setrange(_active, "armor", 1.0)
playerDownB.setrange(_active, "stun_self", False)
playerDownB.setrange(_active, "stun_other", 0)

playerDownB.setrange(_endlag, "attack", 0.0)
playerDownB.setrange(_endlag, "vel_self", Vec2(0, 0))
playerDownB.setrange(_endlag, "vel_other", Vec2(0, 0))
playerDownB.setrange(_endlag, "gravity", 1.0)
playerDownB.setrange(_endlag, "armor", 0.0)
playerDownB.setrange(_endlag, "stun_self", False)
playerDownB.setrange(_endlag, "stun_other", 0)

playerNeutralB = FrameSequence(70)
_startlag = range(0, 5)
_active = range(5, 65)
_endlag = range(65, 70)

playerNeutralB.setrange(_startlag, "attack", 0.0)
playerNeutralB.setrange(_startlag, "vel_self", Vec2(0, 0))
playerNeutralB.setrange(_startlag, "vel_other", Vec2(0, 0))
playerNeutralB.setrange(_startlag, "gravity", 0.5)
playerNeutralB.setrange(_startlag, "armor", 0.2)
playerNeutralB.setrange(_startlag, "stun_self", True)
playerNeutralB.setrange(_startlag, "stun_other", 0)

playerNeutralB.setrange(_active, "attack", 0.0)
playerNeutralB.setrange(_active, "vel_self", Vec2(0, 0))
playerNeutralB.setrange(_active, "vel_other", Vec2(0, 0))
playerNeutralB.setrange(_active, "gravity", 0.0)
playerNeutralB.setrange(_active, "armor", -0.5) # You take more damage if you get attacked
playerNeutralB.setrange(_active, "stun_self", True)
playerNeutralB.setrange(_active, "stun_other", 0)

playerNeutralB.setrange(_endlag, "attack", 0.0)
playerNeutralB.setrange(_endlag, "vel_self", Vec2(0, 0))
playerNeutralB.setrange(_endlag, "vel_other", Vec2(0, 0))
playerNeutralB.setrange(_endlag, "gravity", 1.0)
playerNeutralB.setrange(_endlag, "armor", 0.0)
playerNeutralB.setrange(_endlag, "stun_self", True)
playerNeutralB.setrange(_endlag, "stun_other", 0)

def healhook(pl, frame):
  pl.damage -= 15
  if pl.damage < 0:
    pl.damage = 0

playerNeutralB.addhook(healhook, 69)

animIdle = Animation.load_keyframes("player/idle", 4, 15)
animHurt = Animation.load_keyframes("player/hurt", 4, 3)

animMoveStart = Animation.load_keyframes("player/movestart", 3, 3)
animMoveStart.flag = "move"
animMoveActive = Animation.load_keyframes("player/moveactive", 8, 3)
animMoveActive.flag = "move"
animMoveEnd = Animation.load_keyframes("player/moveend", 3, 3)
animMoveEnd.flag = "move"

animJumpStart = Animation.load_keyframes("player/jumpstart", 3, 3)
animJumpStart.flag = "jumpstart"
animJumpActive = Animation.load_single("player/jumpstart@2")
animJumpEnd = Animation.load_keyframes("player/jumpend", 4, 3)

_tmp = Animation.load_keyframes("player/neutralatk", 4, 2)
animAtkNeutral = Animation(70)
for i in range(len(animAtkNeutral.frames)):
  animAtkNeutral.frames[i] = _tmp.frames[i % len(_tmp.frames)]

# TODO add tools
animAtkUpStart = Animation.load_single("player/upatkstart")
animAtkUpActive = Animation.load_single("player/upatkactive")
animAtkUpEnd = Animation.load_single("player/upatkend")
animAtkDown = Animation.load_single("player/downatk", len(playerDownB.frames))
animAtkForward = Animation.load_single("player/forwardatk", len(playerSideB.frames))