import requests
import sys
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(description='request to run Python code remotely')
    parser.add_argument('-p', type=int, default=1234,
                        help='port number to connect to on the host')
    parser.add_argument('hostname',
                        help='host to which to send our command request')
    parser.add_argument('command',
                        help='command to run on the remote host')
    args = parser.parse_args()
    url = 'https://{}:{}/'.format(args.hostname, args.p)
    pem_path = 'selfsigned.pem'
    r = requests.post(url, args.command, cert=pem_path, verify=pem_path)
    sys.stdout.write(r.text)
