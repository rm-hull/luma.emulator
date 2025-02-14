#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2024 Richard Hull and contributors
# See LICENSE.rst for details.

from .helpers import test_font


def primitives(device, draw):
    padding = 2
    shape_width = 20
    top = padding
    bottom = device.height - padding - 1
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    x = padding
    draw.ellipse((x, top, x + shape_width, bottom), outline="red", fill="black")
    x += shape_width + padding
    draw.rectangle((x, top, x + shape_width, bottom), outline="blue", fill="black")
    x += shape_width + padding
    draw.polygon([(x, bottom), (x + shape_width / 2, top), (x + shape_width, bottom)], outline="green", fill="black")
    x += shape_width + padding
    draw.line((x, bottom, x + shape_width, top), fill="yellow")
    draw.line((x, top, x + shape_width, bottom), fill="yellow")
    x += shape_width + padding
    draw.text((x, top), 'Hello', font=test_font, fill="cyan")
    draw.text((x, top + 20), 'World!', font=test_font, fill="purple")
