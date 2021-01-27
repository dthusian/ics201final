# build.py: Project buildscript
# Concatenates all the files and submit them as one.

import sys

concatOrder = [
  # Comment Documentation
  "doc.py",

  # POD Classes:
  "base.py",
  "hitbox.py",
  "frames.py",
  "game.py",

  # Libraries:
  "display.py",
  "texture.py",
  "framedef.py",

  # Engines:
  "gameview.py",
  "frameengine.py",
  "physicsengine.py",
  "gameengine.py",
  "uiengine.py"

  # Main:
  "main.py"
]

def getlineattr(line):
  tmp0 = str(line).partition(";")[0].strip()
  if tmp0 and tmp0[0] == "\"" and tmp0[-1] == "\"":
    tmp1 = tmp0[1:-1]
    return tmp1.split(" ")
  else:
    return []

def isnonfunctional(line):
  return len(line.strip()) == 0 or line.strip()[0] == "#"

with open("dist.py", "w") as outf:
  for path in concatOrder:
    srcpath = "src/" + path
    print("Concat %s" % path)
    outf.write("### %s\n" % path)
    with open(srcpath, "r") as fp:
      for line in fp:
        attr = getlineattr(line)
        if "ignore" not in attr:
          if len(sys.argv) > 1 and sys.argv[1] == "optimize":
            if not isnonfunctional(line):
              outf.write(line)
          else:
            outf.write(line)
    outf.write("\n")