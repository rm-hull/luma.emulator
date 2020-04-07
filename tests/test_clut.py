#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for :py:class:`luma.emulator.clut`.
"""

from luma.emulator.clut import rgb2short


def test_rgb2short():
    assert rgb2short(100, 100, 100) == 59
