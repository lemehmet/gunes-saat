import sys

import pyglet
from pyglet.gl import *
from PIL import Image, ImageDraw
import six

from pyglet.image.codecs.pil import PILImageDecoder

WIDTH = 128
HEIGHT = 64

window = pyglet.window.Window(visible=False, resizable=True)
image = Image.new('1', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)


def dump_image(msg):
    image_buffer = image.tobytes()
    ibuffer = []
    for b in image_buffer:
        for i in range(8):
            ibuffer.append(255 if b & 0xF0 else 0)
            b <<= 1
    print(f"{msg}: {image.width} x {image.height} = {len(image_buffer)} -> {len(ibuffer)}")
    s = ""
    print(
        "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567")
    nb = b''.join(list(map(lambda x: six.int2byte(x), ibuffer)))
    for i in range(len(nb)):
        if i != 0 and (i % image.width) == 0:
            print(s)
            s = ""
        s += "." if nb[i] == 0 else "|"
    return nb


@window.event
def on_draw():
    ibuffer = dump_image("OnDraw")
    img = pyglet.image.ImageData(image.width, image.height, 'L', ibuffer, pitch=-image.width * 1)
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    background.blit_tiled(0, 0, 0, window.width, window.height)
    img.blit(window.width // 2, window.height // 2, 0)


if __name__ == '__main__':
    # img = pyglet.image.load("display-image", file=image, decoder=PILImageDecoder())
    dump_image("Empty")
    draw.rectangle((1, 1, 40, 20), outline=255, fill=1)
    ibuffer = dump_image("With a rect")
    img = pyglet.image.ImageData(image.width, image.height, 'G', ibuffer, pitch=-image.width * 1)
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

    checks = pyglet.image.create(32, 32, pyglet.image.CheckerImagePattern())
    background = pyglet.image.TileableTexture.create_for_image(checks)

    # Enable alpha blending, required for image.blit.
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    window.width = img.width
    window.height = img.height
    window.set_visible()

    pyglet.app.run()
