#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for :py:class:`luma.emulator.device.asciiart`.
"""

from luma.core.render import canvas
from luma.emulator.device import asciiart

import curses
from helpers import patch

import baseline_data


@patch('curses.start_color')
@patch('curses.use_default_colors')
@patch('curses.noecho')
@patch('curses.echo')
@patch('curses.cbreak')
@patch('curses.nocbreak')
@patch('curses.endwin')
@patch('curses.init_pair')
@patch('curses.color_pair')
@patch('curses.initscr')
def test_asciiart_display(scr, *mocks):
    curses.COLORS = 10
    scr.return_value.getmaxyx.return_value = [40, 80]
    device = asciiart()
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    # TODO: need some asserts somewhere here..

    device.cleanup()
