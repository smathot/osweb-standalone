#!/usr/bin/env python3
# coding=utf-8

import os
import argparse
import base64

SRC_JS = [
    'src/js/vendors~osweb.bundle.js',
    'src/js/osweb.bundle.js',
    'src/js/run-standalone.js'
]
SRC_TMPL = 'src/html/index-standalone.tmpl.html'
DST_DIR = 'public_html'


def read(path):

    print('Reading {}'.format(path))
    with open(path) as fd:
        return fd.read()


def b64(path):

    with open(path, 'rb') as fd:
        e = base64.b64encode(fd.read())
        return e.decode()


def build(src_osexp, fullscreen, log_url, dest):

    print('Building {}\nfullscreen: {}\nlog_url: {}'.format(
        src_osexp, fullscreen, log_url
    ))
    js = '\n'.join([read(path) for path in SRC_JS])
    html = (
        read(SRC_TMPL).format(
            javascript=js,
            osexp_blob=b64(src_osexp)
        )
        .replace('{fullscreen}', 'true' if fullscreen else 'false')
        .replace(
            '{log_url}',
            'null' if not log_url else '\'{}\''.format(log_url)
        )
    )
    if not os.path.exists(DST_DIR):
        os.mkdir(DST_DIR)
    with open(os.path.join(DST_DIR, dest), 'w') as fd:
        fd.write(html)
    print('Successfully built in {}'.format(DST_DIR))


def parse_cmdline():

    parser = argparse.ArgumentParser(description='Build an osweb experiment')
    parser.add_argument(
        'osexp',
        metavar='osexp',
        type=str,
        help='An osexp file'
    )
    parser.add_argument(
        '--fullscreen',
        dest='fullscreen',
        action='store_const',
        const=True, default=False,
        help='Fullscreen mode'
    )
    parser.add_argument(
        '--log_url',
        metavar='log_url',
        type=str,
        default=None,
        help='A url for data logging'
    )
    parser.add_argument(
        '--dest',
        metavar='dest',
        type=str,
        default='index.html',
        help='The name of the HTML file to be generated in public_html'
    )
    args = parser.parse_args()
    return args.osexp, args.fullscreen, args.log_url, args.dest


if __name__ == '__main__':

    build(*parse_cmdline())
