#!/usr/bin/env python3
# coding=utf-8

import os
import argparse
import base64

SRC_JS = [
    'src/js/vendors~osweb.3e1e018192e3bf0e173a.bundle.js',
    'src/js/osweb.66c60ad5c703deb9270f.bundle.js',
]
JS_STANDALONE = 'src/js/run-standalone.js'
JS_JATOS = 'src/js/run-jatos.js'
JS_QUALTRICS = 'src/js/run-qualtrics.js'
TMPL_STANDALONE = 'src/html/index-standalone.tmpl.html'
TMPL_JATOS = 'src/html/index-jatos.tmpl.html'
TMPL_QUALTRICS = 'src/html/index-qualtrics.tmpl.html'
DST_DIR = 'public_html'


def read(path):

    print('Reading {}'.format(path))
    with open(path) as fd:
        return fd.read()


def b64(path):

    with open(path, 'rb') as fd:
        e = base64.b64encode(fd.read())
        return e.decode()


def build(src_osexp, fullscreen, log_url, output, dest, subject):

    print(
        'Building {}\nfullscreen: {}\nlog_url: {}\ndest: {}\nsubject: {}'
        .format(src_osexp, fullscreen, log_url, dest, subject)
    )
    # Determine subject number code. This is a list of subject numbers, followed
    # by a random choice, like so:
    # [10, 11, 12][Math.floor(Math.random()*3)]
    try:
        subjects = [int(s) for s in subject.split(',')]
    except ValueError:
        raise ValueError('Subject numbers should be integers')
    subject_code = '{}[Math.floor(Math.random()*{})]'.format(
        subjects, len(subjects)
    )
    # Determine JS template
    if dest == 'standalone':
        src_js = SRC_JS + [JS_STANDALONE]
        tmpl = TMPL_STANDALONE
    elif dest == 'jatos':
        src_js = SRC_JS + [JS_JATOS]
        tmpl = TMPL_JATOS
    elif dest == 'qualtrics':
        raise NotImplementedError('qualtrics is not yet supported')
    else:
        raise ValueError(
            'Invalid --dest, should be standalone, jatos, or qualtrics'
        )
    js = '\n'.join([read(path) for path in src_js])
    # Fill in the templates
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
        .replace('{subject}', subject_code)
    )
    # Write the output file
    if not os.path.exists(DST_DIR):
        os.mkdir(DST_DIR)
    with open(os.path.join(DST_DIR, output), 'w') as fd:
        fd.write(html)
    print('Successfully built as {}'.format(os.path.join(DST_DIR, output)))


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
        '--output',
        metavar='output',
        type=str,
        default='index.html',
        help='The name of the HTML file to be generated in public_html'
    )
    parser.add_argument(
        '--dest',
        metavar='dest',
        default='standalone',
        help='standalone, jatos, or qualtrics'
    )
    parser.add_argument(
        '--subject',
        metavar='subject',
        type=str,
        default='0',
        help=
            'A comma-separated list of subject numbers. One subject number is '
            'randomly chosen.'
    )
    args = parser.parse_args()
    return (
        args.osexp,
        args.fullscreen,
        args.log_url,
        args.output,
        args.dest,
        args.subject
    )


if __name__ == '__main__':

    build(*parse_cmdline())
