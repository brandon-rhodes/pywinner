import boto.ec2
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

downloads = [

    # Microsoft Windows SDK for Windows 7 and .NET Framework 3.5 SP1
    # Microsoft Windows SDK for Windows 7 and .NET Framework 4

    ('winsdk_35.exe', 'http://download.microsoft.com/download/A/6/A/A6AC035D-DA3F-4F0C-ADA4-37C8E5D34E3D/winsdk_web.exe'),
    ('winsdk_40.exe', 'http://download.microsoft.com/download/7/A/B/7ABD2203-C472-4036-8BA0-E505528CCCB7/winsdk_web.exe'),

    # Python

    'https://www.python.org/ftp/python/2.6.6/python-2.6.6.msi',
    'https://www.python.org/ftp/python/2.6.6/python-2.6.6.amd64.msi',
    'https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi',
    'https://www.python.org/ftp/python/2.7.6/python-2.7.6.amd64.msi',
    'https://www.python.org/ftp/python/3.3.5/python-3.3.5.msi',
    'https://www.python.org/ftp/python/3.3.5/python-3.3.5.amd64.msi',
    'https://www.python.org/ftp/python/3.4.1/python-3.4.1.msi',
    'https://www.python.org/ftp/python/3.4.1/python-3.4.1.amd64.msi',

    ]

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

    for filename, url in targets:
        if filename.startswith('python-'):
            pieces = filename.replace('-', '').split('.')
            bits = '64' if filename.endswith('.amd64.msi') else '32'
            directory = 'C:\\{}{}_{}'.format(pieces[0], pieces[1], bits)
            yield ('Start-Process'
                   ' -FilePath "msiexec.exe"'
                   ' -ArgumentList "/i {} /qn ALLUSERS=1 TARGETDIR={}"'
                   ' -Wait'
                   ' -Passthru'
                   .format(filename, directory))
            # yield 'msiexec /i {} /qn ALLUSERS=1 TARGETDIR={}'.format(
            #     filename, directory)

    yield '</powershell>'

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
    main()
