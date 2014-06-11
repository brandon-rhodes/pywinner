import requests
import sys
from argparse import ArgumentParser

get = r"""\

from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

f = BytesIO(urlopen(
    'https://github.com/brandon-rhodes/pyephem/archive/v3.7.5.3.zip').read())

ZipFile(f).extractall('\\')
"""

build_old = r"""

from subprocess import Popen, PIPE, STDOUT

with open(r'\Users\Administrator\.pypirc', 'w') as f:
    f.write({pypirc_repr})

with open(r'\tmp.bat', 'w') as f:
    f.write(r'''

CD \pyephem-3.7.5.3
SET HOME=\Users\Administrator
CALL "C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\bin\vcvars{bits}.bat"
\python{version}\python.exe setup.py bdist_wininst {upload}

''')

p = Popen(r'\tmp.bat', stdout=PIPE, stderr=STDOUT)
print(p.stdout.read().decode('ascii'))

"""

build_new = r"""

from subprocess import Popen, PIPE, STDOUT

with open(r'\Users\Administrator\.pypirc', 'w') as f:
    f.write({pypirc_repr})

with open(r'\tmp.bat', 'w') as f:
    f.write(r'''

@call "\Program Files\Microsoft SDKs\Windows\v7.1\Bin\SetEnv" /{x} /release

CD \pyephem-3.7.5.3
SET DISTUTILS_USE_SDK=1
\python{version}\python.exe setup.py bdist_wininst {upload}

''')

p = Popen(r'\tmp.bat', stdout=PIPE, stderr=STDOUT)
print(p.stdout.read().decode('ascii'))

"""

def main():
    parser = ArgumentParser(description='build')
    parser.add_argument('-p', type=int, default=1234,
                        help='port number to connect to on the host')
    parser.add_argument('-u', action='store_true',
                        help='upload after each successful build')
    parser.add_argument('hostname',
                        help='host to which to send our command request')
    args = parser.parse_args()
    url = 'https://{}:{}/'.format(args.hostname, args.p)
    pem_path = 'selfsigned.pem'

    with open('/home/brandon/.pypirc') as f:
        pypirc = f.read()

    for version in ('26', '26_64', '27', '27_64',
                    '32', '32_64', '33', '33_64', '34', '34_64'):
        bits = '64' if version.endswith('_64') else '32'
        build = build_old if (version < '33') else build_new
        upload = 'upload' if args.u else ''
        x = 'x86' if (bits == '32') else 'x64'
        command = build.format(bits=bits, version=version,
                               pypirc_repr=repr(pypirc), upload=upload, x=x)
        r = requests.post(url, command, cert=pem_path, verify=pem_path)
        sys.stdout.write(r.text)
        if r.text.startswith('Exception:'):
            print
            print('-' * 72)
            print(command)
            print('-' * 72)
            print('Error while running the above command')
            print('Exiting')
            exit(1)

if __name__ == '__main__':
    main()
