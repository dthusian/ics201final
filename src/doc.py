"""
READ THIS BEFORE READING REST OF PROGRAM

This comment helps you understand how this program works.

# Section 1: Engines

The game is composed of a bunch of "Engines". Each Engine has a
few methods that it may or may not implement:

def process_keys(keys):
def press_key(key):
def release_key(key):
def tick():
def draw():

These functions are used to a) deliver human input to the engine,
or b) to allow the code to run every frame.

tick() will update the state in the Engine. It should be run 60 times
per second (60 Hz). draw() will draw the contents to the screen.

process_keys() receives a dictionary of "Key ID Strings" (more on that
later) indicating which keys are pressed. THis function should also be
called 60 times per second, preferably before tick().

press_key() and release_key() notify the Engine that a key has been
pressed/released. This too, is a "Key ID String".

# Section 2: Key ID Strings

Key ID Strings are a keyboard-agnostic way to identify player inputs.
The dict named `controls_map` defines how keyboard keys map to Key IDs
Key IDs are things like "player1.atk", which represent abstract actions
instead of keys.

# Section 3: Frame Sequences and Animations

A Frame Sequence defines a list of Attack Frames. An Attack Frame is an
object that defines how the player will interact in one moment in time.
It contains attributes such as attack, armor, and gravity. For example,
when a player collides with another player, the game will look at the
attack value on the player's current Attack Frame.

An Animation is similar but distinct. An Animation is a sequence of images
that is used to draw a player. Animations only contain image data and thus
are not used for damage and physics calculations.
"""