# -*- coding: utf-8 -*-
# Copyright (c) 2017-2023 Richard Hull and contributors
# See LICENSE.rst for details.

import sys
import hashlib
from pathlib import Path
from io import StringIO
from contextlib import contextmanager


def md5(fname):
    with open(fname, 'rb') as fp:
        return hashlib.md5(fp.read()).hexdigest()


def get_reference_image(fname):
    """
    Get absolute path for ``fname``.

    :param fname: Filename.
    :type fname: str or pathlib.Path
    :rtype: str
    """
    return str(Path(__file__).resolve().parent.joinpath('reference', fname))


def assert_identical(rname, fname):
    """
    Files that are compared have the same MD5 hash.

    :param rname: Reference file location.
    :type rname: str
    :param fname: Target file location.
    :type fname: str
    """
    reference = get_reference_image(rname)
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
