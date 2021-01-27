"ignore"; from base import *

## Section: Hitboxes

# Represents a circular hitbox.
class CircleHitbox(object):
  center: Vec2
  radius: float
  def __init__(self, cent, rad):
    typeassert(cent, Vec2)
    typeassertmany(rad, [float, int])
    self.center = cent
    self.radius = float(rad)

  # Checks if a point is inside the hitbox
  def contains_point(self, point):
    typeassert(point, Vec2)
    diff = self.center - point
    distsq = diff * diff
    return (distsq.x + distsq.y) < self.radius ** 2

  # Returns the smallest AABB that contains the circle
  def as_AABB(self):
    return AABBHitbox(self.center, Vec2(self.radius, self.radius) * 2)

# Represents an Axis-Aligned Bounding Box,
# which is just a fancy term for "rectangular hitbox"
class AABBHitbox(object):
  center: Vec2
  size: Vec2
  def __init__(self, cent, siz):
    typeassert(cent, Vec2)
    typeassert(siz, Vec2)
    self.center = cent
    self.size = siz

  # Same function as the one in CircularHitbox
  def contains_point(self, point):
    typeassert(point, Vec2)
    diff = self.center - point
    sized2 = self.size / Vec2(2, 2)
    return abs(diff.x) < sized2.x and abs(diff.y) < sized2.y

## Section: Collision Detection

# Checks if 2 circle hitboxes are touching.
# Users should not call this method. They should call touching()
# instead.
def touching_circle(self, box):
  typeassert(box, CircleHitbox)
  typeassert(self, CircleHitbox)
  diff = self.center - box.center
  distsq = diff * diff
  return (distsq.x + distsq.y) < ((self.radius + box.radius) / 2) ** 2

# Checks if 2 circle AABBs are touching.
# Users should not call this method. They should call touching()
# instead.
def touching_aabb(self, box):
  typeassert(box, AABBHitbox)
  typeassert(self, AABBHitbox)
  diff = self.center - box.center
  total_size = self.size + box.size
  return abs(diff.x) < total_size.x and abs(diff.y) < total_size.y

# Generates the 6 hitboxes required to check if
# an AABB and circle are touching.
# See this: https://gamedev.stackexchange.com/a/120897
def generate_mixed_touching_checks(circle, aabb):
  typeassert(circle, CircleHitbox)
  typeassert(aabb, AABBHitbox)
  boxes = []
  boxes.append(AABBHitbox(aabb.center, Vec2(aabb.size.x, aabb.size.y + circle.radius * 2)))
  boxes.append(AABBHitbox(aabb.center, Vec2(aabb.size.x + circle.radius * 2, aabb.size.y)))
  for i in range(4):
    bx = i & 1
    by = i & 2
    sx = 1
    sy = 1
    if bx: sx = -1
    if by: sy = -1
    circle2 = CircleHitbox(aabb.center + Vec2(sx, sy) * aabb.size / Vec2(2, 2), circle.radius)
    boxes.append(circle2)
  return boxes

# Checks if a circle and an AABB are touching.
# Users should not call this method. They should call touching()
# instead.
def touching_mixed(circle, aabb):
  typeassert(circle, CircleHitbox)
  typeassert(aabb, AABBHitbox)
  prebox = AABBHitbox(aabb.center, aabb.size + Vec2(circle.radius * 2, circle.radius * 2))
  if not prebox.contains_point(circle.center): return False
  boxes = generate_mixed_touching_checks(circle, aabb)
  for box in boxes:
    if box.contains_point(circle.center):
      break
  else:
    return False
  return True

# Checks if two hitboxes are touching.
# This function should be called by users.
# It automagically routes combinations of circle and 
# AABB arguments to the appropriate functions.
def touching(a, b):
  typeassertmany(a, [CircleHitbox, AABBHitbox])
  typeassertmany(b, [CircleHitbox, AABBHitbox])
  ca = typeeq(a, CircleHitbox)
  cb = typeeq(b, CircleHitbox)
  if ca and cb:
    return touching_circle(a, b)
  if not (ca or cb):
    return touching_aabb(a, b)
  if ca and not cb:
    return touching_mixed(a, b)
  if cb and not ca:
    return touching_mixed(b, a)