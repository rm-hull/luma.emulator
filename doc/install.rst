Installation
------------
.. note:: The library has been tested against Python 3.6 and newer.

System packages
^^^^^^^^^^^^^^^

Install dependencies for pygame first::

  $ sudo apt install python3-dev python3-pip build-essential
  $ sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev

And upgrade ``pip`` and ``setuptools``::

  $ sudo -H pip install --upgrade --ignore-installed pip setuptools

Installing from PyPi
^^^^^^^^^^^^^^^^^^^^

Install the latest version of the luma.emulator library directly from
`PyPI <https://pypi.python.org/pypi?:action=display&name=luma.emulator>`_::

  $ sudo -H pip install --upgrade luma.emulator
