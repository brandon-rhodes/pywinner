"""Command-line interface for pywinner."""

from __future__ import print_function

import os
import sys
from argparse import ArgumentParser
from subprocess import check_output
from tempfile import NamedTemporaryFile

parser = ArgumentParser(description='HTTPS eval() server')
subs = parser.add_subparsers(dest='subcommand')

sub = subs.add_parser('generate',
                      description='Generate a self-signed SSL certificate')
sub.add_argument('-b', nargs='?', type=int, default=2187,
                 help='number of RSA bits to generate (default: 2187)')
sub.add_argument('filename', nargs='?', default='selfsigned.pem',
                 help='file to which to write the PEM certificate and key')

args = parser.parse_args()

if args.subcommand == 'generate':
    if os.path.exists('selfsigned.pem'):
        print('Error: file selfsigned.pem already exists', file=sys.stderr)
        sys.exit(1)
    with NamedTemporaryFile() as f:
        cert_text = check_output([
            'openssl', 'req', '-new', '-newkey', 'rsa:{}'.format(args.b),
            '-nodes', '-x509', '-keyout', f.name,
            '-subj', '/C=US/ST=Ohio/L=Bluffton/O=pywinner/CN=selfsigned',
            ])
        key_text = f.read()
    with open('selfsigned.pem', 'wb') as f:
        f.write(cert_text + key_text)
