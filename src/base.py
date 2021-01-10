import time

## Section: Type handling library

def typeassert(obj, typ):
  if type(obj) != typ:
    raise TypeError("Object " + str(obj) + " is not of type " + str(typ))

def typeassertmany(obj, typs):
  if type(obj) not in typs:
    raise TypeError("Object " + str(obj) + " is not the correct type!")

def typeeq(obj, typ):
  return type(obj) == typ

## Section: Logging

def translate_loglevel(lvl):
  if lvl == -1: return "DEBUG"
  if lvl ==  0: return "INFO"
  if lvl ==  1: return "WARNING"
  if lvl ==  2: return "ERROR"
  if lvl ==  3: return "REALLY REALLY BAD"
  return "???"

def ics_log(level, thing):
  ctime = time.gmtime()
  print("[{:02}:{:02}:{:02}] [{}] {}".format(ctime.tm_hour, ctime.tm_min, ctime.tm_sec, translate_loglevel(level), thing))

"const"; LOGLEVEL_DEBUG      = -1
"const"; LOGLEVEL_INFO       = 0
"const"; LOGLEVEL_WARNING    = 1
"const"; LOGLEVEL_ERROR      = 2
"const"; LOGLEVEL_ARMAGEDDON = 3

## Section: Vector

class Vec2(object):
  x: float
  y: float
  def __init__(self, nx, ny):
    typeassertmany(nx, [float, int])
    typeassertmany(nx, [float, int])
    self.x = float(nx)
    self.y = float(ny)

  def clone(self):
    return Vec2(self.x, self.y)
  
  def __add__(self, other):
    typeassert(other, Vec2)
    return Vec2(self.x + other.x, self.y + other.y)
  
  def __sub__(self, other):
    typeassert(other, Vec2)
    return Vec2(self.x - other.x, self.y - other.y)
  
  def __mul__(self, other):
    typeassert(other, Vec2)
    return Vec2(self.x * other.x, self.y * other.y)
  
  def __truediv__(self, other):
    typeassert(other, Vec2)
    return Vec2(self.x / other.x, self.y / other.y)
  
  def as_tuple(self):
    return (self.x, self.y)

  @staticmethod
  def from_tuple(vec):
    return Vec2(vec[0], vec[1])