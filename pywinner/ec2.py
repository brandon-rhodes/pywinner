import boto.ec2
import pkg_resources
import time

region = 'us-east-1'

# image_id = 'ami-88de32e0'  # 64-bit
# image_id = 'ami-f6de329e'  # 32-bit

# "Windows_Server-2012-RTM-English-64Bit-Base-2014.05.14"
image_id = 'ami-aede32c6'

def main():
    user_data = build_user_data()
    with open('setup.ps1', 'w') as f:
        f.write('\r\n'.join(generate_powershell_script(include_cert=False)))
    return
    start_instance(user_data)

# The following list of URLs drives downloading and installing several
# versions of Python plus two Windows SDKs.

downloads = [

    # Microsoft Windows SDK for Windows 7 and .NET Framework 3.5 SP1
    # Microsoft Windows SDK for Windows 7 and .NET Framework 4

    (r'\Users\Administrator\Desktop\visual_studio_2008_express.exe', 'http://go.microsoft.com/?linkid=7729279'),
    (r'\Users\Administrator\Desktop\winsdk_35.exe', 'http://download.microsoft.com/download/7/A/B/7ABD2203-C472-4036-8BA0-E505528CCCB7/winsdk_web.exe'),
    (r'\Users\Administrator\Desktop\winsdk_40.exe', 'http://download.microsoft.com/download/A/6/A/A6AC035D-DA3F-4F0C-ADA4-37C8E5D34E3D/winsdk_web.exe'),

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

    # ('source.zip', 'https://github.com/brandon-rhodes/pyephem/archive/v3.7.5.3.zip'),

    ]

def download_targets():
    for thing in downloads:
        if isinstance(thing, tuple):
            filename, url = thing
        else:
            url = thing
            filename = url.rsplit('/', 1)[-1]
        yield filename, url

def generate_powershell_script(include_cert=True):
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
            directory = r'C:\{}{}{}'.format(pieces[0], pieces[1], suffix)
            yield ('Start-Process'
                   ' -FilePath "msiexec.exe"'
                   ' -ArgumentList "/i {} /qn ALLUSERS=1 TARGETDIR={}"'
                   ' -Wait'
                   ' -Passthru'
                   .format(filename, directory))

    servertext = pkg_resources.resource_string(__name__, 'server.py')
    if '\r\n' not in servertext:
        servertext = servertext.replace('\n', '\r\n')

    if include_cert:
        yield r'$pemtext = @"'
        with open('selfsigned.pem') as f:
            yield '\r\n'.join(f.read().split('\n'))
        yield r'"@'
        yield r'$pemtext | Out-File -FilePath \selfsigned.pem -Encoding ASCII'

    yield r'$servertext = @"'
    yield servertext
    yield r'"@'
    yield r'$servertext | Out-File -FilePath \server.py -Encoding ASCII'

    yield (r'Start-Process'
           r' -FilePath'
           r' \python34\python.exe'
           r' -ArgumentList "\server.py \selfsigned.pem"')

    # Turn off Windows Firewall so we can communicate on port 1234

    yield ('Set-NetFirewallProfile'
           ' -Profile Domain,Public,Private'
           ' -Enabled False')

def build_user_data():
    return '<powershell>\r\n{}\r\n</powershell>\r\n'.format(
        '\r\n'.join(generate_powershell_script()))

def start_instance(user_data):
    connection = boto.ec2.connect_to_region(region)
    reservation = connection.run_instances(
        image_id, key_name='win', security_groups=['win1234'],
        instance_type='m3.large', user_data=user_data,
        )
    instance = reservation.instances[0]
    status = instance.update()
    while status == 'pending':
        time.sleep(1)
        status = instance.update()
    print instance.id
    print instance.public_dns_name
    instance.add_tag('Name', 'pywinner')

if __name__ == '__main__':
    main()
