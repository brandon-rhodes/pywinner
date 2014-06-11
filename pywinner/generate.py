"""Command-line interface for pywinner."""

from __future__ import print_function

import os
import sys
from argparse import ArgumentParser
from subprocess import check_output
from tempfile import NamedTemporaryFile

def generate(numbits, path):
    if os.path.exists(path):
        print('Error: file {!r} already exists'.format(path), file=sys.stderr)
        sys.exit(1)
    with NamedTemporaryFile() as f:
        cert_text = check_output([
            'openssl', 'req', '-new', '-newkey', 'rsa:{}'.format(numbits),
            '-nodes', '-x509', '-keyout', f.name,
            '-subj', '/C=US/ST=Ohio/L=Bluffton/O=pywinner/CN=*.compute-1.amazonaws.com',
            ])
        key_text = f.read()
    with open(path, 'wb') as f:
        f.write(cert_text + key_text)

if __name__ == '__main__':
    parser = ArgumentParser(
        description='Generate a self-signed SSL certificate')
    parser.add_argument('-b', nargs='?', type=int, default=2187,
                        help='number of RSA bits to generate (default: 2187)')
    parser.add_argument('filename', nargs='?', default='selfsigned.pem',
                        help='where to write the PEM certificate and key')
    args = parser.parse_args()
    generate(args.b, args.filename)
