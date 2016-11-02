# laser-development-kit

## Requirements

* [Koheron Laser board](https://www.koheron.com/laser-development-kit)
* Red Pitaya board with the [latest release](https://github.com/Koheron/koheron-sdk/releases/) installed on the SD card
* Python (2.7+ or 3.5+) with Numpy and Scipy
* koheron-python (`pip install koheron`)
* PyQtGraph (`pip install pyqtgraph`) - only for the Graphical User Interface

[How to set up a network connection for the Red Pitaya and find its IP address.](https://www.koheron.com/support/redpitaya-ip-address)

## Script examples

```sh
export HOST=192.168.1.100 # Red Pitaya IP address
python examples/power_vs_current.py
```

[See more examples](https://github.com/Koheron/laser-development-kit/tree/master/examples).

## Graphical User Interface

```sh
python interface.py
```

![Demo](https://cloud.githubusercontent.com/assets/1735094/9765362/317e8212-5714-11e5-8480-ab3e311260c9.gif)

## Build your custom instrument

You can build custom instruments using reference designs in the [koheron-sdk](https://github.com/Koheron/koheron-sdk) repository.

## Copyright

Copyright 2015-2016 Koheron SAS. The code is released under [the MIT licence](https://github.com/Koheron/laser-development-kit/blob/master/LICENSE).
