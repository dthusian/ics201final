import time

## Section: Type handling library
# Functions that enforce type-safety.
# (As you can tell, I am a fan of statically-typed languages)

# Checks an object's type, and throws if it doesn't match
def typeassert(obj, typ):
  if type(obj) != typ:
    raise TypeError("Object " + str(obj) + " is not of type " + str(typ))


# Checks an object's type for any of the provided types.
# Throws only if it matches none of them.
def typeassertmany(obj, typs):
  if type(obj) not in typs:
    raise TypeError("Object " + str(obj) + " is not the correct type!")

# Checks an object's type, and does not throw.
# Returns True if the type matches, and False otherwise.
def typeeq(obj, typ):
  return type(obj) == typ

## Section: Logging

# Translates a log constant into a human-readable string.
# Normally not called by users.
# For example, translate_loglevel(LOGLEVEL_DEBUG) would return "DEBUG"
# Returns "???" if an invalid value is passed.
def translate_loglevel(lvl):
  if lvl == -1: return "DEBUG"
  if lvl ==  0: return "INFO"
  if lvl ==  1: return "WARNING"
  if lvl ==  2: return "ERROR"
  if lvl ==  3: return "REALLY REALLY BAD"
  return "???"

# Logs a message to the console.
def ics_log(level, thing):
  ctime = time.gmtime()
  print("[{:02}:{:02}:{:02}] [{}] {}".format(ctime.tm_hour, ctime.tm_min, ctime.tm_sec, translate_loglevel(level), thing))

# Constants that represent log levels.
"const"; LOGLEVEL_DEBUG      = -1
"const"; LOGLEVEL_INFO       = 0
"const"; LOGLEVEL_WARNING    = 1
"const"; LOGLEVEL_ERROR      = 2
"const"; LOGLEVEL_ARMAGEDDON = 3

## Section: Vector

# Represents a Vector with 2 components.
# This is a staple of any good game engine.
# Math works on the Vec2 class.
# This class is like the Zelle's Graphics Point class.
class Vec2(object):
  x: float
  y: float

  # Constructs a Vec2 with the two given components.
  # Can accept floats or ints as input
  def __init__(self, nx, ny):
    typeassertmany(nx, [float, int])
    typeassertmany(nx, [float, int])
    self.x = float(nx)
    self.y = float(ny)

  # Clones the Vector.
  def clone(self):
    return Vec2(self.x, self.y)
  
  # Arithmetic functions on the vectors
  # Arithmetic is element-wise and works as one would expect.
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

  def __repr__(self):
    return f"Vec2({self.x}, {self.y})"

  # Converts a tuple with 2 components into an equivalent vector.
  @staticmethod
  def from_tuple(vec):
    return Vec2(vec[0], vec[1])