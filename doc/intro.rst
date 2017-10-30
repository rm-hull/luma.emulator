Introduction
------------

There are various display emulators available for running code against, for debugging
and screen capture functionality:

* The :py:class:`luma.emulator.device.capture` device will persist a numbered PNG file to
  disk every time its ``display`` method is called.

* The :py:class:`luma.emulator.device.gifanim` device will record every image when its ``display``
  method is called, and on program exit (or Ctrl-C), will assemble the images into an
  animated GIF.

* The :py:class:`luma.emulator.device.pygame` device uses the `pygame` library to
  render the displayed image to a pygame display surface.

Check out the `examples <https://github.com/rm-hull/luma.examples/blob/master/README.rst#emulators>`__
on how to use the luma.emulator devices.
