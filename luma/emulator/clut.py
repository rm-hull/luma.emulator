# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

# From a comment by @TerrorBite on https://gist.github.com/MicahElliott/719710

# Default color levels for the color cube
cubelevels = [0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff]

# Generate a list of midpoints of the above list
snaps = [(x + y) / 2 for x, y in list(zip(cubelevels, [0] + cubelevels))[1:]]


def rgb2short(r, g, b):
    """
    Converts RGB values to the nearest equivalent xterm-256 color.
    """
    # Using list of snap points, convert RGB value to cube indexes
    r, g, b = [len(tuple(s for s in snaps if s < x)) for x in (r, g, b)]

    # Simple colorcube transform
    return (r * 36) + (g * 6) + b + 16


class __memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


rgb2short = __memoize(rgb2short)
