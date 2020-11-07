# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

import os
import sys
import struct

try:
    import fcntl
    import termios
    import curses
    ASCII_AVAILABLE = True
except ImportError:
    # If running on windows, these package are not available!
    ASCII_AVAILABLE = False
import atexit
import logging
import string
import collections
from io import StringIO
from PIL import Image, ImageFont, ImageDraw

from luma.core.device import device
from luma.core.interface.serial import noop
from luma.emulator.render import transformer
from luma.emulator.clut import rgb2short
from luma.emulator.segment_mapper import regular


logger = logging.getLogger(__name__)

__all__ = ["capture", "gifanim", "pygame"]


class emulator(device):
    """
    Base class for emulated display driver classes
    """
    def __init__(self, width, height, rotate, mode, transform, scale):
        super(emulator, self).__init__(serial_interface=noop())
        try:
            import pygame
        except ImportError:
            raise RuntimeError("Emulator requires pygame to be installed")
        self._pygame = pygame
        self.capabilities(width, height, rotate, mode)
        self.scale = 1 if transform == "none" else scale
        self._transform = getattr(transformer(pygame, width, height, scale),
                                  "none" if scale == 1 else transform)
        self._contrast = 1.0
        self._last_image = None
        self.segment_mapper = regular

    def show(self):
        self.contrast(0xFF)

    def hide(self):
        self.contrast(0x00)

    def contrast(self, value):
        assert(0 <= value <= 255)
        self._contrast = value / 255.0
        if self._last_image is not None:
            self.display(self._last_image)

    def cleanup(self):
        pass

    def to_surface(self, image, alpha=1.0):
        """
        Converts a :py:mod:`PIL.Image` into a :class:`pygame.Surface`,
        transforming it according to the ``transform`` and ``scale``
        constructor arguments.
        """
        assert(0.0 <= alpha <= 1.0)
        if alpha < 1.0:
            im = image.convert("RGBA")
            black = Image.new(im.mode, im.size, "black")
            im = Image.blend(black, im, alpha)
        else:
            im = image.convert("RGB")

        mode = im.mode
        size = im.size
        data = im.tobytes()
        del im

        surface = self._pygame.image.fromstring(data, size, mode)
        return self._transform(surface)


class capture(emulator):
    """
    Pseudo-device that acts like a physical display, except that it writes the
    image to a numbered PNG file when the :func:`display` method is called.
    Supports 24-bit color depth.
    """
    def __init__(self, width=128, height=64, rotate=0, mode="RGB",
                 transform="scale2x", scale=2, file_template="luma_{0:06}.png",
                 **kwargs):
        super(capture, self).__init__(width, height, rotate, mode, transform, scale)
        self._count = 0
        self._file_template = file_template

    def display(self, image):
        """
        Takes a :py:mod:`PIL.Image` and dumps it to a numbered PNG file.
        """
        assert(image.size == self.size)
        self._last_image = image

        self._count += 1
        filename = self._file_template.format(self._count)
        image = self.preprocess(image)
        surface = self.to_surface(image, alpha=self._contrast)
        logger.debug(f"Writing: {filename}")
        self._pygame.image.save(surface, filename)


class gifanim(emulator):
    """
    Pseudo-device that acts like a physical display, except that it collects
    the images when the :func:`display` method is called, and on exit,
    assembles them into an animated GIF image. Supports 24-bit color depth,
    albeit with an indexed color palette.
    """
    def __init__(self, width=128, height=64, rotate=0, mode="RGB",
                 transform="scale2x", scale=2, filename="luma_anim.gif",
                 duration=0.01, loop=0, max_frames=None, **kwargs):
        super(gifanim, self).__init__(width, height, rotate, mode, transform, scale)
        self._images = []
        self._count = 0
        self._max_frames = max_frames
        self._filename = filename
        self._loop = loop
        self._duration = int(duration * 1000)
        atexit.register(self.write_animation)

    def display(self, image):
        """
        Takes an image, scales it according to the nominated transform, and
        stores it for later building into an animated GIF.
        """
        assert(image.size == self.size)
        self._last_image = image

        image = self.preprocess(image)
        surface = self.to_surface(image, alpha=self._contrast)
        rawbytes = self._pygame.image.tostring(surface, "RGB", False)
        im = Image.frombytes("RGB", surface.get_size(), rawbytes)
        self._images.append(im)

        self._count += 1
        logger.debug("Recording frame: {0}".format(self._count))

        if self._max_frames and self._count >= self._max_frames:
            sys.exit(0)

    def write_animation(self):
        if len(self._images) > 0:
            logger.debug("Please wait... building animated GIF")
            with open(self._filename, "w+b") as fp:
                self._images[0].save(fp, save_all=True, loop=self._loop,
                                     duration=self._duration,
                                     append_images=self._images[1:],
                                     optimize=True, format="GIF")

            file_size = os.stat(self._filename).st_size
            logger.debug("Wrote {0} frames to file: {1} ({2} bytes)".format(
                self._count, self._filename, file_size))


class pygame(emulator):
    """
    Pseudo-device that acts like a physical display, except that it renders
    to a displayed window. The frame rate is limited to 60FPS (much faster
    than a Raspberry Pi can achieve, but this can be overridden as necessary).
    Supports 24-bit color depth.

    :mod:`pygame` is used to render the emulated display window, and it's
    event loop is checked to see if the ESC key was pressed or the window
    was dismissed: if so :func:`sys.exit()` is called.
    """
    def __init__(self, width=128, height=64, rotate=0, mode="RGB", transform="scale2x",
                 scale=2, frame_rate=60, **kwargs):
        super(pygame, self).__init__(width, height, rotate, mode, transform, scale)
        self._pygame.display.init()
        self._pygame.font.init()
        self._pygame.display.set_caption("Luma.core Display Emulator")
        self._clock = self._pygame.time.Clock()
        self._fps = frame_rate
        self._screen = None

    def _abort(self):
        keystate = self._pygame.key.get_pressed()
        return keystate[self._pygame.K_ESCAPE] or self._pygame.event.peek(self._pygame.QUIT)

    def display(self, image):
        """
        Takes a :py:mod:`PIL.Image` and renders it to a pygame display surface.
        """
        assert(image.size == self.size)
        self._last_image = image

        image = self.preprocess(image)
        self._clock.tick(self._fps)
        self._pygame.event.pump()

        if self._abort():
            self._pygame.quit()
            sys.exit()

        surface = self.to_surface(image, alpha=self._contrast)
        if self._screen is None:
            self._screen = self._pygame.display.set_mode(surface.get_size())
        self._screen.blit(surface, (0, 0))
        self._pygame.display.flip()


if ASCII_AVAILABLE:
    __all__.extend(["asciiart", "asciiblock"])

    class asciiart(emulator):
        """
        Pseudo-device that acts like a physical display, except that it converts the
        image to display into an ASCII-art representation and downscales colors to
        match the xterm-256 color scheme. Supports 24-bit color depth.

        This device takes hold of the terminal window (using curses), and any output
        for sysout and syserr is captured and stored, and is replayed when the
        cleanup method is called.

        Loosely based on https://github.com/ajalt/pyasciigen/blob/master/asciigen.py

        .. versionadded:: 0.2.0
        """
        def __init__(self, width=128, height=64, rotate=0, mode="RGB", transform="scale2x",
                     scale=2, **kwargs):

            super(asciiart, self).__init__(width, height, rotate, mode, transform, scale)
            self._stdscr = curses.initscr()
            curses.start_color()
            curses.use_default_colors()
            for i in range(0, curses.COLORS):
                curses.init_pair(i, i, -1)
            curses.noecho()
            curses.cbreak()

            # Capture all stdout, stderr
            self._old_stdX = (sys.stdout, sys.stderr)
            self._captured = (StringIO(), StringIO())
            sys.stdout, sys.stderr = self._captured

            # Sort printable characters according to the number of black pixels present.
            # Don't use string.printable, since we don't want any whitespace except spaces.
            charset = (string.ascii_letters + string.digits + string.punctuation + "  ")
            self._chars = list(reversed(sorted(charset, key=self._char_density)))
            self._char_width, self._char_height = ImageFont.load_default().getsize("X")
            self._contrast = 1.0

        def _char_density(self, c, font=ImageFont.load_default()):
            """
            Count the number of black pixels in a rendered character.
            """
            image = Image.new('1', font.getsize(c), color=255)
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), c, fill="white", font=font)
            return collections.Counter(image.getdata())[0]  # 0 is black

        def _generate_art(self, image, width, height):
            """
            Return an iterator that produces the ascii art.
            """
            # Characters aren't square, so scale the output by the aspect ratio of a charater
            height = int(height * self._char_width / float(self._char_height))
            image = image.resize((width, height), Image.ANTIALIAS).convert("RGB")

            for (r, g, b) in image.getdata():
                greyscale = int(0.299 * r + 0.587 * g + 0.114 * b)
                ch = self._chars[int(greyscale / 255. * (len(self._chars) - 1) + 0.5)]
                yield (ch, rgb2short(r, g, b))

        def display(self, image):
            """
            Takes a :py:mod:`PIL.Image` and renders it to the current terminal as
            ASCII-art.
            """
            assert(image.size == self.size)
            self._last_image = image

            surface = self.to_surface(self.preprocess(image), alpha=self._contrast)
            rawbytes = self._pygame.image.tostring(surface, "RGB", False)
            image = Image.frombytes("RGB", surface.get_size(), rawbytes)

            scr_width = self._stdscr.getmaxyx()[1]
            scale = float(scr_width) / image.width

            self._stdscr.erase()
            self._stdscr.move(0, 0)
            try:
                for (ch, color) in self._generate_art(image, int(image.width * scale), int(image.height * scale)):
                    self._stdscr.addstr(ch, curses.color_pair(color))

            except curses.error:
                # End of screen reached
                pass

            self._stdscr.refresh()

        def cleanup(self):
            super(asciiart, self).cleanup()

            # Stty sane
            curses.nocbreak()
            curses.echo()
            curses.endwin()

            # Restore stdout & stderr, then print out captured
            sys.stdout, sys.stderr = self._old_stdX
            sys.stdout.write(self._captured[0].getvalue())
            sys.stdout.flush()
            sys.stderr.write(self._captured[1].getvalue())
            sys.stderr.flush()

    class asciiblock(emulator):
        """
        Pseudo-device that acts like a physical display, except that it converts
        the image pixels to display into colored ASCII half-blocks (ASCII code 220,
        '▄'), where the upper part background is used for one pixel, and the lower
        part foreground is used for the pixel on the next row. As most terminal
        display characters are in ratio 2:1, the half-block appears square.

        Inspired by `Command Line Curiosities - Making the Terminal Sing by Hamza Haiken <https://www.youtube.com/watch?v=j5zA5Xi_ph8>`__

        .. versionadded:: 1.1.0
        """
        def __init__(self, width=128, height=64, rotate=0, mode="RGB", transform="scale2x",
                     scale=2, **kwargs):

            super(asciiblock, self).__init__(width, height, rotate, mode, transform, scale)
            self._CSI("2J")

        def _terminal_size(self):
            s = struct.pack('HHHH', 0, 0, 0, 0)
            t = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s)
            return struct.unpack('HHHH', t)

        def _generate_art(self, image, width, height):
            """
            Return an iterator that produces the ascii art.
            """
            image = image.resize((width, height), Image.ANTIALIAS).convert("RGB")
            pixels = list(image.getdata())

            for y in range(0, height - 1, 2):
                for x in range(width):
                    i = y * width + x
                    bg = rgb2short(*(pixels[i]))
                    fg = rgb2short(*(pixels[i + width]))
                    yield (fg, bg)

        def _CSI(self, cmd):
            """
            Control sequence introducer
            """
            sys.stdout.write('\x1b[')
            sys.stdout.write(cmd)

        def display(self, image):
            """
            Takes a :py:mod:`PIL.Image` and renders it to the current terminal as
            ASCII-blocks.
            """
            assert(image.size == self.size)
            self._last_image = image

            surface = self.to_surface(self.preprocess(image), alpha=self._contrast)
            rawbytes = self._pygame.image.tostring(surface, "RGB", False)
            image = Image.frombytes("RGB", surface.get_size(), rawbytes)

            scr_width = self._terminal_size()[1]
            scale = float(scr_width) / image.width

            self._CSI('1;1H')  # Move to top/left

            for (fg, bg) in self._generate_art(image, int(image.width * scale), int(image.height * scale)):
                self._CSI('38;5;{0};48;5;{1}m'.format(fg, bg))
                sys.stdout.write('▄')

            self._CSI('0m')
            sys.stdout.flush()

        def cleanup(self):
            super(asciiblock, self).cleanup()
            self._CSI('0m')
            self._CSI('2J')
