Installation
------------
.. note:: The library has been tested against Python 2.7 and 3.4+.

   For **Python3** installation, substitute the following in the
   instructions below.

   * ``pip`` ⇒ ``pip3``, 
   * ``python`` ⇒ ``python3``, 
   * ``python-dev`` ⇒ ``python3-dev``,
   * ``python-pip`` ⇒ ``python3-pip``.

System packages
^^^^^^^^^^^^^^^

Install dependencies for pygame first::

  $ sudo apt install python-dev python-pip build-essential
  $ sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev

And upgrade ``pip`` and ``setuptools``::

  $ sudo -H pip install --upgrade --ignore-installed pip setuptools

Installing from PyPi
^^^^^^^^^^^^^^^^^^^^

Install the latest version of the luma.emulator library directly from
`PyPI <https://pypi.python.org/pypi?:action=display&name=luma.emulator>`_::

  $ sudo -H pip install --upgrade luma.emulator
