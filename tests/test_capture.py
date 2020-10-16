#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for :py:class:`luma.emulator.device.capture`.
"""

from tempfile import NamedTemporaryFile

from luma.core.render import canvas
from luma.emulator.device import capture

import baseline_data
from helpers import assert_identical


def test_display():
    with NamedTemporaryFile(suffix='.png', delete=True) as temp:
        fname = temp.name
        device = capture(file_template=fname, transform="none")

        # Use the same drawing primitives as the demo
        with canvas(device) as draw:
            baseline_data.primitives(device, draw)

        assert_identical('capture.png', fname)
