# OSWEB

Copyright 2018 Sebastiaan Mathôt (@smathot)

## About

OSWeb is an online runtime for OpenSesame experiments:

- <https://github.com/shyras/osweb/>

This repository contains a simple script that packages the OSWeb runtime into a standalone `index.html` plus a `.osexp` file with the experiment.

## Usage

~~~
usage: build.py [-h] [--fullscreen] [--log_url log_url] osexp

Build an osweb experiment

positional arguments:
  osexp              An osexp file

optional arguments:
  -h, --help         show this help message and exit
  --fullscreen       Fullscreen mode
  --log_url log_url  A url for data logging
~~~

## License

OSWeb is distributed under the terms of the GNU General Public License 3. The full license should be included in the file COPYING, or can be obtained from:

- <http://www.gnu.org/licenses/gpl.txt>
