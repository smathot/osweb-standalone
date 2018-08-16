#!/usr/bin/env python3
# coding=utf-8

import os
import argparse
import base64

SRC_JS = [
    'src/js/vendors~osweb.bundle.js',
    'src/js/osweb.bundle.js',
]
JS_STANDALONE = 'src/js/run-standalone.js'
JS_JATOS = 'src/js/run-jatos.js'
TMPL_STANDALONE = 'src/html/index-standalone.tmpl.html'
TMPL_JATOS = 'src/html/index-jatos.tmpl.html'
DST_DIR = 'public_html'


def read(path):

    print('Reading {}'.format(path))
    with open(path) as fd:
        return fd.read()


def b64(path):

    with open(path, 'rb') as fd:
        e = base64.b64encode(fd.read())
        return e.decode()


def build(src_osexp, fullscreen, log_url, dest, jatos):

    print('Building {}\nfullscreen: {}\nlog_url: {}\njatos: {}'.format(
        src_osexp, fullscreen, log_url, jatos
    ))
    src_js = SRC_JS + [JS_JATOS if jatos else JS_STANDALONE]
    tmpl = TMPL_JATOS if jatos else TMPL_STANDALONE
    js = '\n'.join([read(path) for path in src_js])
    html = (
        read(tmpl).format(
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
    print('Successfully built as {}'.format(os.path.join(DST_DIR, dest)))


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
        const=True,
        default=False,
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
    parser.add_argument(
        '--jatos',
        metavar='jatos',
        action='store_const',
        const=True,
        default=False,
        help='Indicates that the output file should be made for JATOS'
    )
    args = parser.parse_args()
    return args.osexp, args.fullscreen, args.log_url, args.dest, args.jatos


if __name__ == '__main__':

    build(*parse_cmdline())
