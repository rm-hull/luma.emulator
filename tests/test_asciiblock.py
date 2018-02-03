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
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from luma.core.render import canvas
from luma.emulator.device import asciiblock

import baseline_data
from helpers import patch, md5


def noop():
    pass


def test_display():
    scr_height = 40
    scr_width = 100
    fake_result = struct.pack('HHHH', scr_height, scr_width, 600, 616)

    orig = sys.stdout
    sys.stdout = StringIO()
    sys.stdout.fileno = lambda: 1

    with patch('fcntl.ioctl', return_value=fake_result):
        device = asciiblock()
        with canvas(device) as draw:
            baseline_data.primitives(device, draw)

    device.cleanup = noop

    out = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = orig

    if sys.version_info > (3, 0):
        out = out.encode('utf-8')

    digest = hashlib.md5(out).hexdigest()
    assert md5('tests/reference/asciiblock.txt') == digest
