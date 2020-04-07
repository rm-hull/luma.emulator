#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for :py:class:`luma.emulator.render.transformer`.
"""

import pygame

from PIL import Image, ImageChops
from luma.core.device import dummy
from luma.core.render import canvas
from luma.emulator.render import transformer

from helpers import get_reference_image


def baseline_im():
    return pygame.image.load(get_reference_image("capture.png"))


def to_pillow_img(surface):
    s = pygame.image.tostring(surface, "RGB", False)
    return Image.frombytes("RGB", (surface.get_width(), surface.get_height()), s)


def to_pygame_surface(im):
    return pygame.image.fromstring(im.tobytes(), im.size, im.mode)


def test_none():
    with open(get_reference_image("capture.png"), "rb") as fp:
        ref = Image.open(fp)
        surface = baseline_im()
        tf = transformer(pygame, 128, 64, 1)
        im = to_pillow_img(tf.none(surface))
        bbox = ImageChops.difference(ref, im).getbbox()
        assert bbox is None


def test_scale2x():
    with open(get_reference_image("scale2x.png"), "rb") as fp:
        ref = Image.open(fp)
        surface = baseline_im()
        tf = transformer(pygame, 128, 64, 2)
        im = to_pillow_img(tf.scale2x(surface))
        bbox = ImageChops.difference(ref, im).getbbox()
        assert bbox is None


def test_smoothscale():
    with open(get_reference_image("smoothscale.png"), "rb") as fp:
        ref = Image.open(fp)
        surface = baseline_im()
        tf = transformer(pygame, 128, 64, 2)
        im = to_pillow_img(tf.smoothscale(surface))
        bbox = ImageChops.difference(ref, im).getbbox()
        assert bbox is None


def test_identity():
    with open(get_reference_image("identity.png"), "rb") as fp:
        ref = Image.open(fp)
        surface = baseline_im()
        tf = transformer(pygame, 128, 64, 2)
        im = to_pillow_img(tf.identity(surface))
        bbox = ImageChops.difference(ref, im).getbbox()
        assert bbox is None


def test_led_matrix():
    with open(get_reference_image("led_matrix.png"), "rb") as fp:
        ref = Image.open(fp)
        device = dummy(width=40, height=24)
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white")
            draw.text((5, 2), "Hello", fill="white")
            draw.text((5, 10), "World", fill="white")
        surface = to_pygame_surface(device.image)
        tf = transformer(pygame, device.width, device.height, 16)
        im = to_pillow_img(tf.led_matrix(surface))
        bbox = ImageChops.difference(ref, im).getbbox()
        assert bbox is None


def test_seven_segment():
    with open(get_reference_image("seven_segment.png"), "rb") as fp:
        ref = Image.open(fp)
        chars = [
            # Alphabet with omissions
            0x00, 0x01, 0x08, 0x02, 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f,
            0x70, 0x7f, 0x7b, 0x7d, 0x1f, 0x0d, 0x3d, 0x6f, 0x47, 0x7b, 0x17,
            0x10, 0x18, 0x06, 0x15, 0x1d, 0x67, 0x73, 0x05, 0x5b, 0x0f, 0x1c,
            0x1c, 0x3b, 0x6d, 0x77, 0x7f, 0x4e, 0x7e, 0x4f, 0x47, 0x5e, 0x37,
            0x30, 0x38, 0x0e, 0x76, 0x7e, 0x67, 0x73, 0x46, 0x5b, 0x0f, 0x3e,
            0x3e, 0x3b, 0x6d, 0x80, 0x80
        ]
        device = dummy(width=len(chars), height=8)
        with canvas(device) as draw:
            for x in range(len(chars)):
                val = chars[x]
                for y in range(8):
                    mask = 1 << y
                    if val & mask != 0:
                        draw.point((device.width - x, y), fill="white")
        surface = to_pygame_surface(device.image)
        tf = transformer(pygame, device.width, device.height, 16)
        im = to_pillow_img(tf.seven_segment(surface))
        bbox = ImageChops.difference(ref, im).getbbox()
        assert bbox is None
