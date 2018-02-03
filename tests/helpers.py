# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

from contextlib import contextmanager
import hashlib
import os.path
import sys

if sys.version_info > (3, 0):
    from io import StringIO
else:
    from io import BytesIO as StringIO


try:
    from unittest.mock import call, patch
except ImportError:
    from mock import call, patch, Mock  # noqa: F401


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
