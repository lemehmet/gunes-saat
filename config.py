import platform

# True if running on raspberry pi
RASPI = platform.machine().startswith("armv") and platform.system() == "Linux"
# Forces running code in UI emulation even on RasPi, helpful to test on a raspberry desktop
FORCE_EMU = False
# Use (pyglet) emulator to show display. Arrow keys = Joystick, A = A, Z = B, SPACE = C (Joystick center)
USE_EMU = True if not RASPI else True if FORCE_EMU else False
# Width and height in pixels
WIDTH = 128
HEIGHT = 64
PAGES = HEIGHT // 8
# Background and foreground colors to use. Either black (0) or white (255)
BG = 0
FG = 255
# Nominal font size for clock, below font list has a normalization factor since font heights wildy vary
CLOCK_FONT_SIZE = 18
# Print performance metrics every second, or not. This doesn't add much of a lag but keeps printing.
SHOW_STATS = True
# Changing views are done with sliding animations, how many steps are required to complete the animation
HSLIDING_STEPS = 16
# Finer vertical granularity than the page size is PITA
VSLIDING_STEPS = 8
VSLIDING_STEPS = HEIGHT // 8 if VSLIDING_STEPS > (HEIGHT // 8) else VSLIDING_STEPS

# Font file names, as appear in the fonts folder, size coefficient
FONTS = [
    ('04B_30__.TTF', 1.0),              # 0
    ('Minecraftia-Regular.ttf', 1.2),   # 1
    ('pixelmix.ttf', 1.2),              # 2
    ('Retron2000.ttf', 1.4),            # 3
    ('slkscr.ttf', 1.4),                # 4
    ('Squarewave-Italic.ttf', 2.0),     # 5
    ('Squarewave.ttf', 2.0),            # 6
    ('VCR_OSD_MONO_1.001.ttf', 1.0),    # 7
    ('3Dventure.ttf', 1.5),             # 8
    ('04B_19__.TTF', 1.5),              # 9
    ('advanced_pixel_lcd-7.ttf', 0.8),  # 10
    ('Alkhemikal.ttf', 2.0),            # 11
    ('cube.ttf', 1.0),                  # 12
    ('DigitalDisco-Thin.ttf', 1.8),     # 13
    ('edunline.ttf', 1.4),              # 14
    ('m04.TTF', 0.7),                   # 15
    ('Nintendo-DS-BIOS.ttf', 2.0),      # 16
    ('Perfect-DOS-VGA-437.ttf', 1.2),   # 17
    ('PIXEARG_.TTF', 1.0),              # 18
    ('pixelpoiiz.ttf', 1.2),            # 19
    ('Pokemon Classic.ttf', 0.8),       # 20
    ('Super-Mario-Bros--3.ttf', 1.0),   # 21
    ('Vermin Vibes 1989.ttf', 2.0),     # 22
    ('Aardvark Cwm Type.ttf', 2.5),     # 23
    ('BMNEA___.TTF', 1.6),              # 24
    ('BMSTA___.TTF', 0.8),              # 25
    ('Extrude.ttf', 1.8),               # 26
    ('GhastlyPixe.ttf', 1.6),           # 27
    ('GrapeSoda.ttf', 1.8),             # 28
    ('ice_pixel-7.ttf', 1.8),           # 29
    ('m20.TTF', 1.0),                   # 30
    ('Pixel-Noir.ttf', 1.0),            # 31
    ('Pixeled English Font.ttf', 1.2),  # 32
    ('TINYBBA_.TTF', 1.0),              # 33
    ('V5_bloques.ttf', 0.8),            # 34
]

print(f"Running on raspi: {RASPI}, using emu: {USE_EMU}")

# Button mappings
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
