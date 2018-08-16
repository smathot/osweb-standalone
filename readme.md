# OSWEB

Copyright 2018 Sebastiaan Mathôt (@smathot)

## About

OSWeb is an online runtime for OpenSesame experiments:

- <https://github.com/shyras/osweb/>

This repository contains a simple script that packages the OSWeb runtime and an experiment into a standalone `.html` file that can be loaded directly into a browser.

## Usage

~~~
usage: build.py [-h] [--fullscreen] [--log_url log_url] [--dest dest]
                [--jatos]
                osexp

Build an osweb experiment

positional arguments:
  osexp              An osexp file

optional arguments:
  -h, --help         show this help message and exit
  --fullscreen       Fullscreen mode
  --log_url log_url  A url for data logging
  --dest dest        The name of the HTML file to be generated in public_html
  --jatos            Indicates that the output file should be made for JATOS
~~~

## Logging

If you specify a log url, this will be called every time that the `logger` item is executed. The to-be-logged variables are simply appended as a JSON string to the URL.


## License

OSWeb is distributed under the terms of the GNU General Public License 3. The full license should be included in the file COPYING, or can be obtained from:

- <http://www.gnu.org/licenses/gpl.txt>
