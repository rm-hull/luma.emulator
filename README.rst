`luma.core <https://github.com/rm-hull/luma.core>`__ **|** 
`luma.docs <https://github.com/rm-hull/luma.docs>`__ **|** 
luma.emulator **|** 
`luma.examples <https://github.com/rm-hull/luma.examples>`__ **|** 
`luma.lcd <https://github.com/rm-hull/luma.lcd>`__ **|** 
`luma.led_matrix <https://github.com/rm-hull/luma.led_matrix>`__ **|** 
`luma.oled <https://github.com/rm-hull/luma.oled>`__ 

Luma.Emulator
=============

.. image:: https://github.com/rm-hull/luma.emulator/workflows/luma.emulator/badge.svg?branch=master
   :target: https://github.com/rm-hull/luma.emulator/actions?workflow=luma.emulator

.. image:: https://coveralls.io/repos/github/rm-hull/luma.emulator/badge.svg?branch=master
   :target: https://coveralls.io/github/rm-hull/luma.emulator?branch=master

.. image:: https://img.shields.io/pypi/pyversions/luma.emulator.svg
   :target: https://pypi.python.org/pypi/luma.emulator

.. image:: https://img.shields.io/pypi/v/luma.emulator.svg
   :target: https://pypi.python.org/pypi/luma.emulator

.. image:: https://img.shields.io/pypi/dm/luma.emulator
   :target: https://pypi.python.org/project/luma.emulator

.. image:: https://img.shields.io/maintenance/yes/2020.svg?maxAge=2592000

**luma.emulator** provides a series of pseudo-display devices which allow 
the `luma.core <https://github.com/rm-hull/luma.core>`_ components to be used
without running a physical device. These include:

* Real-time (pixel) emulator, based on `pygame <http://pygame.org/docs/>`__
* LED matrix and 7-segment renderers
* PNG screen capture
* Animated GIF animator
* Real-time ASCII-art & block emulators

Documentation
-------------
Documentation can be found on https://luma-emulator.readthedocs.io.

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/clock_anim.gif?raw=true
   :alt: clock

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/invaders_anim.gif?raw=true
   :alt: invaders

.. image:: https://raw.githubusercontent.com/rm-hull/luma.oled/master/doc/images/crawl_anim.gif?raw=true
   :alt: crawl

.. image:: https://raw.githubusercontent.com/rm-hull/luma.emulator/master/doc/images/ascii-art.png?raw=true
   :alt: asciiart

.. image:: https://raw.githubusercontent.com/rm-hull/luma.led_matrix/master/doc/images/emulator.gif
   :alt: max7219 emulator

License
-------
The MIT License (MIT)

Copyright (c) 2017-2020 Richard Hull and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
