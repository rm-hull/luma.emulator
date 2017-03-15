#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for luma.emulator.
"""

import os.path
from tempfile import NamedTemporaryFile

from luma.core.render import canvas
from luma.emulator.device import capture, gifanim, emulator

import pytest

import baseline_data
from helpers import patch, get_reference_image, md5


def test_emulator_pygame_missing():
    with patch.dict('sys.modules', {'pygame': None}):
        with pytest.raises(RuntimeError) as ex:
            emulator(1, 2, 3, 4, 5, 6)
        assert str(ex.value) == 'Emulator requires pygame to be installed'


def test_capture_display():
    reference = get_reference_image('capture.png')

    fname = NamedTemporaryFile(suffix=".png").name
    device = capture(file_template=fname, transform="none")

    # Use the same drawing primitives as the demo
    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    assert md5(reference) == md5(fname)


def test_gifanim_write():
    reference = get_reference_image('anim.gif')

    fname = NamedTemporaryFile(suffix=".gif").name
    device = gifanim(filename=fname)

    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    with canvas(device) as draw:
        draw.text((30, 10), text="Blipvert", fill="white")

    with canvas(device) as draw:
        baseline_data.primitives(device, draw)

    device.write_animation()
    assert md5(reference) == md5(fname)


def test_gifanim_noimages():
    fname = NamedTemporaryFile(suffix=".gif").name
    device = gifanim(filename=fname)
    device.write_animation()
    assert not os.path.exists(fname)
