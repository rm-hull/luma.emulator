#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for :py:class:`luma.emulator.device.asciiblock`.
"""

import sys
import struct
import hashlib
from pathlib import Path
from unittest.mock import patch

from luma.core.render import canvas
import baseline_data
from helpers import md5, redirect_stdout


def noop():
    pass


ASCII_AVAILABLE = True
try:
    from luma.emulator.device import asciiblock
except ImportError:
    ASCII_AVAILABLE = False


def test_display():
    # If ascii art works, then do the test otherwise just end the function call
    if ASCII_AVAILABLE:
        scr_height = 40
        scr_width = 100
        fake_result = struct.pack('HHHH', scr_height, scr_width, 600, 616)

        with redirect_stdout() as f:
            sys.stdout.fileno = lambda: 1
            with patch('fcntl.ioctl', return_value=fake_result):
                device = asciiblock()
                with canvas(device) as draw:
                    baseline_data.primitives(device, draw)

        device.cleanup = noop
        out = f.getvalue().encode('utf-8')

        digest = hashlib.md5(out).hexdigest()
        fname = Path(__file__).resolve().parent.joinpath('reference', 'asciiblock.txt')
        assert md5(str(fname)) == digest


def test_cleanup():
    # If ascii art works, then do the test otherwise just end the function call
    if ASCII_AVAILABLE:
        scr_height = 40
        scr_width = 100
        fake_result = struct.pack('HHHH', scr_height, scr_width, 600, 616)

        with redirect_stdout() as f:
            sys.stdout.fileno = lambda: 1
            with patch('fcntl.ioctl', return_value=fake_result):
                device = asciiblock()
                device.cleanup()

        device.cleanup = noop
        out = f.getvalue().encode('utf-8')

        digest = hashlib.md5(out).hexdigest()
        assert digest == '3139690363a9edf4c03d553b36a37fe6'
