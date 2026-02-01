Installation
------------
.. note:: The library is supported for Python 3

System packages
^^^^^^^^^^^^^^^

Install dependencies for pygame first::

  $ sudo apt install python3-dev python3-pip python3-numpy libfreetype6-dev libjpeg-dev build-essential
  $ sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

Installing from PyPi
^^^^^^^^^^^^^^^^^^^^

You can install the latest version of the luma.emulator library directly from
`PyPI <https://pypi.org/project/luma.emulator>`_.

First, create a `virtual environment <https://docs.python.org/3/library/venv.html>`__::

  $ python3 -m venv ~/luma-env

This creates a virtual environment in the home directory called ``luma-env``
and a Python executable at ``~/luma-env/bin/python``.

Activate the environment::

  $ source ~/luma-env/bin/activate

Finally, install the latest version of the luma.emulator library in the
virtual environment with::

  $ ~/luma-env/bin/python -m pip install luma.emulator
