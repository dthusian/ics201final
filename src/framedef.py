"ignore"; from frames import *

playerUpB = FrameSequence(50)

playerUpB.setall("attack", 2.0)
playerUpB.setall("vel_self", Vec2(0, -4))
playerUpB.setall("vel_other", Vec2(0, -3))
playerUpB.setall("gravity", False)
playerUpB.setall("armor", False)
playerUpB.setall("hook", None)
playerUpB.setall("stun", True)