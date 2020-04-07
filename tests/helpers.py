# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

from contextlib import contextmanager
import hashlib
import os.path
import sys
from io import StringIO


def md5(fname):
    with open(fname, 'rb') as fp:
        return hashlib.md5(fp.read()).hexdigest()


def get_reference_image(fname):
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'reference',
        fname))


def assert_identical(rname, fname):
    reference = get_reference_image(rname)
    assert md5(reference) == md5(fname)


@contextmanager
def redirect_stdout(fileobj=None):
    if fileobj is None:
        fileobj = StringIO()
    orig = sys.stdout
    sys.stdout = fileobj
    try:
        yield fileobj
    finally:
        sys.stdout = orig
