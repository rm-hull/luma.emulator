# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

from pathlib import Path


__all__ = ["transformer"]


class transformer(object):
    """
    Helper class used to dispatch transformation operations.
    """
    def __init__(self, pygame, width, height, scale):
        self._pygame = pygame
        self._input_size = (width, height)
        self._output_size = (width * scale, height * scale)
        self._scale = scale
        base_dir = Path(__file__).resolve().parent
        self._led_on, self._led_off, self._sevenseg = \
            [self._pygame.image.load(str(base_dir.joinpath("images", img)))
             for img in ["led_on.png", "led_off.png", "7-segment.png"]]

    def none(self, surface):
        """
        No-op transform - used when ``scale`` = 1
        """
        return surface

    def scale2x(self, surface):
        """
        Scales using the AdvanceMAME Scale2X algorithm which does a
        'jaggie-less' scale of bitmap graphics.
        """
        assert(self._scale == 2)
        return self._pygame.transform.scale2x(surface)

    def smoothscale(self, surface):
        """
        Smooth scaling using MMX or SSE extensions if available
        """
        return self._pygame.transform.smoothscale(surface, self._output_size)

    def identity(self, surface):
        """
        Fast scale operation that does not sample the results
        """
        return self._pygame.transform.scale(surface, self._output_size)

    def led_matrix(self, surface):
        """
        Transforms the input surface into an LED matrix (1 pixel = 1 LED)
        """
        scale = self._led_on.get_width()
        w, h = self._input_size
        pix = self._pygame.PixelArray(surface)
        img = self._pygame.Surface((w * scale, h * scale))

        for y in range(h):
            for x in range(w):
                led = self._led_on if pix[x, y] & 0xFFFFFF > 0 else self._led_off
                img.blit(led, (x * scale, y * scale))

        return img

    def seven_segment(self, surface):
        w, h = self._input_size
        cw, ch = 30, 50
        pix = self._pygame.PixelArray(surface)
        img = self._pygame.Surface((w * cw, h * ch // 8))

        for x in range(w):
            byte = 0
            for y in range(h - 1):
                byte <<= 1
                if pix[x, y] & 0xFFFFFF > 0:
                    byte |= 1

            # Drop any values > 127
            byte &= 0x7F

            i = (byte % 16) * cw
            j = (byte // 16) * ch

            img.blit(self._sevenseg, ((w - x - 1) * cw, 0), area=self._pygame.Rect(i, j, cw, ch))

        return img
