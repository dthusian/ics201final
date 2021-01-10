# build.py: Project buildscript
# Concatenates all the files and submit them as one.

concatOrder = [
  "base.py",
  "hitbox.py",
  "player.py",
  "game.py",
  "gameview.py",
  "main.py"
]

def getlineattr(line):
  tmp0 = str(line).partition(";")[0].strip()
  if tmp0 and tmp0[0] == "\"" and tmp0[-1] == "\"":
    tmp1 = tmp0[1:-1]
    return tmp1.split(" ")
  else:
    return []

with open("dist.py", "w") as outf:
  for path in concatOrder:
    srcpath = "src/" + path
    print("Concat %s" % path)
    outf.write("### %s\n" % path)
    with open(srcpath, "r") as fp:
      for line in fp:
        attr = getlineattr(line)
        if "ignore" not in attr:
          outf.write(line)
    outf.write("\n")