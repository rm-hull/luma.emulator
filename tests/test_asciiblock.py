#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for :py:class:`luma.emulator.device.asciiblock`.
"""

import hashlib
import struct
import sys

from luma.core.render import canvas
import baseline_data
from helpers import patch, md5, redirect_stdout


def noop():
    pass


try:
    from luma.emulator.device import asciiblock

    def test_display():
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
        out = f.getvalue()

        if sys.version_info > (3, 0):
            out = out.encode('utf-8')

        digest = hashlib.md5(out).hexdigest()
        assert md5('tests/reference/asciiblock.txt') == digest

    def test_cleanup():
        scr_height = 40
        scr_width = 100
        fake_result = struct.pack('HHHH', scr_height, scr_width, 600, 616)

        with redirect_stdout() as f:
            sys.stdout.fileno = lambda: 1
            with patch('fcntl.ioctl', return_value=fake_result):
                device = asciiblock()
                device.cleanup()

        device.cleanup = noop
        out = f.getvalue()

        if sys.version_info > (3, 0):
            out = out.encode('utf-8')

        digest = hashlib.md5(out).hexdigest()
        assert digest == '3139690363a9edf4c03d553b36a37fe6'

except ImportError:
    def test_display():
        # Not available on windows
        pass

    def test_cleanup():
        pass
