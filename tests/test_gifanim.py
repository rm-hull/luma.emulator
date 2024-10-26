#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2024 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for :py:class:`luma.emulator.device.gifanim`.
"""

from pathlib import Path
from tempfile import NamedTemporaryFile

from PIL import Image

from luma.core.render import canvas
from luma.emulator.device import gifanim

import pytest

from .baseline_data import primitives
from .helpers import get_reference_file, test_font, assert_identical


def test_gifanim_write():
    with NamedTemporaryFile(suffix='.gif') as temp:
        fname = temp.name
        device = gifanim(filename=fname)

        with canvas(device) as draw:
            primitives(device, draw)

        with canvas(device) as draw:
            draw.text((30, 10), text="Blipvert", font=test_font, fill="white")

        with canvas(device) as draw:
            primitives(device, draw)

        device.write_animation()
        assert_identical('anim.gif', fname)


def test_gifanim_noimages():
    with NamedTemporaryFile(suffix='.gif') as temp:
        fname = temp.name
        device = gifanim(filename=fname)
        device.write_animation()
    assert not Path(fname).exists()


def test_gifanim_max_frames():
    reference = get_reference_file('anim.gif')
    img = Image.open(reference)
    with NamedTemporaryFile(suffix='.gif') as temp:
        fname = temp.name
        device = gifanim(256, 128, filename=fname, max_frames=1)

        with pytest.raises(SystemExit) as ex:
            device.display(img)
        assert str(ex.value) == '0'
    img.close()
