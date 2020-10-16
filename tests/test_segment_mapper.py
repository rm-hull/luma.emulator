#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Tests for :py:class:`luma.emulator.segment_mapper`.
"""

from luma.emulator.segment_mapper import regular


def test_regular():
    result = [48, 109, 121, 51, 0, 127, 15, 78]
    for index, val in enumerate(regular('1234 BTC')):
        assert val == result[index]
