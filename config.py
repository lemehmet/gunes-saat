import platform

RASPI = platform.machine().startswith("armv") and platform.system() == "Linux"
FORCE_EMU = False # Forces running code in UI emulation even on RasPi
USE_EMU = True if not RASPI else True if FORCE_EMU else False
WIDTH = 128
HEIGHT = 64
BG = 0
FG = 255
CLOCK_FONT_SIZE = 20

FONTS = [
    ('04B_30__.TTF', 1.0),
    ('Minecraftia-Regular.ttf', 1.2),
    ('pixelmix.ttf', 1.2),
    ('Retron2000.ttf', 1.4),
    ('slkscr.ttf', 1.4),
    ('Squarewave-Italic.ttf', 2.0),
    ('Squarewave.ttf', 2.0),
    ('VCR_OSD_MONO_1.001.ttf', 1.0),
]

print(f"Running on raspi: {RASPI}, using emu: {USE_EMU}")

if USE_EMU:
    from pyglet.window import key
    BUTTON_A = key.Z
    BUTTON_B = key.A
    BUTTON_C = key.SPACE
    BUTTON_UP = key.UP
    BUTTON_DOWN = key.DOWN
    BUTTON_LEFT = key.LEFT
    BUTTON_RIGHT = key.RIGHT
else:
    import board
    BUTTON_A = int(board.D5.id)
    BUTTON_B = int(board.D6.id)
    BUTTON_C = int(board.D4.id)
    BUTTON_UP = int(board.D17.id)
    BUTTON_DOWN = int(board.D22.id)
    BUTTON_LEFT = int(board.D27.id)
    BUTTON_RIGHT = int(board.D23.id)

ALL_BUTTONS = [BUTTON_A, BUTTON_B, BUTTON_C, BUTTON_UP, BUTTON_DOWN, BUTTON_LEFT, BUTTON_RIGHT]
