# -*- coding: utf-8 -*-
# Copyright (c) 2017-2024 Richard Hull and contributors
# See LICENSE.rst for details.

import sys
import hashlib
from pathlib import Path
from io import StringIO
from contextlib import contextmanager
from PIL import ImageFont


def md5(fname):
    with open(fname, 'rb') as fp:
        return hashlib.md5(fp.read()).hexdigest()


def get_reference_file(fname):
    """
    Get absolute path for ``fname``.

    :param fname: Filename.
    :type fname: str or pathlib.Path
    :rtype: str
    """
    return str(Path(__file__).resolve().parent.joinpath('reference', fname))


def get_reference_pillow_font(fname):
    """
    Load :py:class:`PIL.ImageFont` type font from provided fname

    :param fname: The name of the file that contains the PIL.ImageFont
    :type fname: str
    :rtype: :py:class:`PIL.ImageFont`
    """
    path = get_reference_file(Path('font').joinpath(fname))
    return ImageFont.load(path)


# font used in (most) tests
test_font = get_reference_pillow_font('courB08.pil')


def assert_identical(rname, fname):
    """
    Files that are compared have the same MD5 hash.

    :param rname: Reference file location.
    :type rname: str
    :param fname: Target file location.
    :type fname: str
    """
    reference = get_reference_file(rname)
    md5_ref = md5(reference)
    md5_target = md5(fname)
    assert md5_ref == md5_target, \
        f"""Generated file is not identical to {rname}
- generated: {fname} (MD5: {md5_target})
- reference: {reference} (MD5: {md5_ref})
        """


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
