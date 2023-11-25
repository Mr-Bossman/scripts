#!/usr/bin/env python3
import sys
from PIL import Image, ImageEnhance
import PIL.ImageOps
import struct

# python3 ~/scripts/printer.py ~/Pictures/unknown.png 512 512 | lpr -P SRP-350plusII

def print_img(im):
	im = im.convert('1')
	sys.stdout.buffer.write(b''.join((bytearray(b'\x1d\x76\x30\x00'),
                                      struct.pack('2B', int(im.size[0] / 8) % 256,
                                                  int(im.size[0] / (8 * 256))),
                                      struct.pack('2B', im.size[1] % 256,
                                                  int(im.size[1] / 256)),
                                      im.tobytes())))

if len(sys.argv) != 4:
	print("./print.py image.png {height} {width}", file=sys.stderr)

image_name = sys.argv[1]
height = int(sys.argv[2])
width = int(sys.argv[3])
im = Image.open(image_name)
im = im.rotate(90, PIL.Image.NEAREST, expand = 1)
im = im.resize((height,width))
im = ImageEnhance.Brightness(im).enhance(1)
im = ImageEnhance.Contrast(im).enhance(3)

im = PIL.ImageOps.invert(im.convert('L'))
print_img(im)
