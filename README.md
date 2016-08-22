# laser-development-kit

[![Circle CI](https://circleci.com/gh/Koheron/laser-development-kit.svg?style=shield)](https://circleci.com/gh/Koheron/laser-development-kit) [![Code Climate](https://codeclimate.com/github/Koheron/laser-development-kit/badges/gpa.svg)](https://codeclimate.com/github/Koheron/laser-development-kit)

#### `Python API for Koheron Laser Development Kit`

## [Get started](https://www.koheron.com/products/laser-development-kit/getting-started/) 

1) Get [latest release](https://github.com/Koheron/zynq-sdk/releases/) of SD card image.
On Windows, you can use [win32diskimager](http://sourceforge.net/projects/win32diskimager/) to burn the SD card.

2) Insert the SD card on the Red Pitaya, then plug ethernet and power cables. 
The last number of the board IP address is displayed on binary format on the 8 Red Pitaya LEDs for convenience.

3) Make sure the following packages are installed:
* Python (2.7+ or 3.5+) with Numpy and Scipy
* Qt (`apt-get install python-qt4`)
* PyQtGraph (`pip install pyqtgraph`)
* requests (`pip install requests`)
* koheron-tcp-client (`pip install koheron`)

4) Launch GUI:

```sh
python interface.py
```

You will need to enter the board IP adress to connect to the board.

![Demo](https://cloud.githubusercontent.com/assets/1735094/9765362/317e8212-5714-11e5-8480-ab3e311260c9.gif)

## Build your custom FPGA bitstream

You can build custom bitstreams from the reference designs in the [koheron-sdk](https://github.com/Koheron/koheron-sdk) repository.

## Copyright

Copyright 2015 Koheron SAS. The code is released under [the MIT licence](https://github.com/Koheron/laser-development-kit/blob/master/LICENSE).

