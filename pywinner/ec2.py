import boto.ec2
import textwrap
import time

region = 'us-east-1'

# image_id = 'ami-88de32e0'  # 64-bit
# image_id = 'ami-f6de329e'  # 32-bit

# "Windows_Server-2012-RTM-English-64Bit-Base-2014.05.14"
image_id = 'ami-aede32c6'

def main():
    user_data = build_user_data()
    print user_data
    #start_instance(user_data)

# The following list of URLs drives downloading and installing several
# versions of Python plus two Windows SDKs.

downloads = [

    # Microsoft Windows SDK for Windows 7 and .NET Framework 3.5 SP1
    # Microsoft Windows SDK for Windows 7 and .NET Framework 4

    ('winsdk_35.exe', 'http://download.microsoft.com/download/7/A/B/7ABD2203-C472-4036-8BA0-E505528CCCB7/winsdk_web.exe'),
    ('winsdk_40.exe', 'http://download.microsoft.com/download/A/6/A/A6AC035D-DA3F-4F0C-ADA4-37C8E5D34E3D/winsdk_web.exe'),

    # Python

    'https://www.python.org/ftp/python/2.5.4/python-2.5.4.msi',
    'https://www.python.org/ftp/python/2.5.4/python-2.5.4.amd64.msi',
    'https://www.python.org/ftp/python/2.6.6/python-2.6.6.msi',
    'https://www.python.org/ftp/python/2.6.6/python-2.6.6.amd64.msi',
    'https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi',
    'https://www.python.org/ftp/python/2.7.6/python-2.7.6.amd64.msi',
    'https://www.python.org/ftp/python/3.0.1/python-3.0.1.msi',
    'https://www.python.org/ftp/python/3.0.1/python-3.0.1.amd64.msi',
    'https://www.python.org/ftp/python/3.1.4/python-3.1.4.msi',
    'https://www.python.org/ftp/python/3.1.4/python-3.1.4.amd64.msi',
    'https://www.python.org/ftp/python/3.2.5/python-3.2.5.msi',
    'https://www.python.org/ftp/python/3.2.5/python-3.2.5.amd64.msi',
    'https://www.python.org/ftp/python/3.3.5/python-3.3.5.msi',
    'https://www.python.org/ftp/python/3.3.5/python-3.3.5.amd64.msi',
    'https://www.python.org/ftp/python/3.4.1/python-3.4.1.msi',
    'https://www.python.org/ftp/python/3.4.1/python-3.4.1.amd64.msi',

    # Thing needing compilation (Later: make a command line param? Or
    # have a powershell script for it right on the Windows box?)

    ('source.zip', 'https://github.com/brandon-rhodes/pyephem/archive/v3.7.5.3.zip'),

    ]

https_server = textwrap.dedent(r"""
    from argparse import ArgumentParser
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from ssl import wrap_socket
    class EvalHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = b'abc\n'
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
    parser = ArgumentParser(description='HTTPS eval() server')
    parser.add_argument('pempath', help='path to PEM certificate+key file')
    args = parser.parse_args()
    h = HTTPServer(('0.0.0.0', 443), EvalHandler)
    h.socket = wrap_socket(h.socket, certfile=args.pempath, server_side=True)
    h.serve_forever()
    """)

def download_targets():
    for thing in downloads:
        if isinstance(thing, tuple):
            filename, url = thing
        else:
            url = thing
            filename = url.rsplit('/', 1)[-1]
        yield filename, url

def generate_user_data():
    yield '<powershell>'

    targets = list(download_targets())

    yield '$wc = New-Object System.Net.WebClient'

    for filename, url in targets:
        yield '$wc.DownloadFile("{}", "{}")'.format(url, filename)

    yield '$shell_app=new-object -com shell.application'
    yield r'$zip_file = $shell_app.namespace((Get-Location).Path + "\source.zip")'
    yield '$destination = $shell_app.namespace((Get-Location).Path)'
    yield '$destination.Copyhere($zip_file.items())'

    for filename, url in targets:
        if filename.startswith('python-'):
            pieces = filename.replace('-', '').split('.')
            suffix = '_64' if (pieces[-2] == 'amd64') else ''
            directory = 'C:\\{}{}{}'.format(pieces[0], pieces[1], suffix)
            yield ('Start-Process'
                   ' -FilePath "msiexec.exe"'
                   ' -ArgumentList "/i {} /qn ALLUSERS=1 TARGETDIR={}"'
                   ' -Wait'
                   ' -Passthru'
                   .format(filename, directory))

    yield '</powershell>'
    return

    # I guess the following commands have to be saved INSIDE a
    # subsequent script to be run later?

    yield 'bat script:'
    yield 'set DISTUTILS_USE_SDK=1'
    yield 'cd pyephem-3.7.5.3'
    for sdk, version in [
            ('v7.0', '26'), ('v7.0', '27'), ('v7.0', '33'), ('v7.1', '34')
            ]:
        for bits, arch in (32, 'x86'), (64, 'x64'):
            yield (r'@call "C:\Program Files\Microsoft SDKs\Windows\{}\Bin'
                   r'\SetEnv.Cmd" /{} /release'.format(sdk, arch))
            c = r'C:\python{}_{}\python.exe setup.py bdist_wininst'.format(
                version, bits)
            if bits == 32 and version.startswith('2'):
                c = c.replace('_32', '')  # Python installer ignores TARGETDIR?
            yield c

def build_user_data():
    return '\r\n'.join(generate_user_data())

def start_instance(user_data):
    connection = boto.ec2.connect_to_region(region)
    reservation = connection.run_instances(
        image_id, key_name='win',
        instance_type='m3.large', user_data=user_data,
        )
    instance = reservation.instances[0]
    status = instance.update()
    while status == 'pending':
        time.sleep(1)
        status = instance.update()
    print instance.id
    print instance.public_dns_name
    #import pdb; pdb.set_trace()

if __name__ == '__main__':
    print(https_server)
    #main()