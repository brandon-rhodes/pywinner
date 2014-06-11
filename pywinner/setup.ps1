$wc = New-Object System.Net.WebClient
$wc.DownloadFile("http://go.microsoft.com/?linkid=7729279", "\Users\Administrator\Desktop\visual_studio_2008_express.exe")
$wc.DownloadFile("http://download.microsoft.com/download/7/A/B/7ABD2203-C472-4036-8BA0-E505528CCCB7/winsdk_web.exe", "\Users\Administrator\Desktop\winsdk_35.exe")
$wc.DownloadFile("http://download.microsoft.com/download/A/6/A/A6AC035D-DA3F-4F0C-ADA4-37C8E5D34E3D/winsdk_web.exe", "\Users\Administrator\Desktop\winsdk_40.exe")
$wc.DownloadFile("https://www.python.org/ftp/python/2.5.4/python-2.5.4.msi", "python-2.5.4.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/2.5.4/python-2.5.4.amd64.msi", "python-2.5.4.amd64.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/2.6.6/python-2.6.6.msi", "python-2.6.6.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/2.6.6/python-2.6.6.amd64.msi", "python-2.6.6.amd64.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi", "python-2.7.6.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/2.7.6/python-2.7.6.amd64.msi", "python-2.7.6.amd64.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.0.1/python-3.0.1.msi", "python-3.0.1.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.0.1/python-3.0.1.amd64.msi", "python-3.0.1.amd64.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.1.4/python-3.1.4.msi", "python-3.1.4.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.1.4/python-3.1.4.amd64.msi", "python-3.1.4.amd64.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.2.5/python-3.2.5.msi", "python-3.2.5.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.2.5/python-3.2.5.amd64.msi", "python-3.2.5.amd64.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.3.5/python-3.3.5.msi", "python-3.3.5.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.3.5/python-3.3.5.amd64.msi", "python-3.3.5.amd64.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.4.1/python-3.4.1.msi", "python-3.4.1.msi")
$wc.DownloadFile("https://www.python.org/ftp/python/3.4.1/python-3.4.1.amd64.msi", "python-3.4.1.amd64.msi")
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-2.5.4.msi /qn ALLUSERS=1 TARGETDIR=C:\python25" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-2.5.4.amd64.msi /qn ALLUSERS=1 TARGETDIR=C:\python25_64" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-2.6.6.msi /qn ALLUSERS=1 TARGETDIR=C:\python26" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-2.6.6.amd64.msi /qn ALLUSERS=1 TARGETDIR=C:\python26_64" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-2.7.6.msi /qn ALLUSERS=1 TARGETDIR=C:\python27" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-2.7.6.amd64.msi /qn ALLUSERS=1 TARGETDIR=C:\python27_64" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.0.1.msi /qn ALLUSERS=1 TARGETDIR=C:\python30" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.0.1.amd64.msi /qn ALLUSERS=1 TARGETDIR=C:\python30_64" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.1.4.msi /qn ALLUSERS=1 TARGETDIR=C:\python31" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.1.4.amd64.msi /qn ALLUSERS=1 TARGETDIR=C:\python31_64" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.2.5.msi /qn ALLUSERS=1 TARGETDIR=C:\python32" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.2.5.amd64.msi /qn ALLUSERS=1 TARGETDIR=C:\python32_64" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.3.5.msi /qn ALLUSERS=1 TARGETDIR=C:\python33" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.3.5.amd64.msi /qn ALLUSERS=1 TARGETDIR=C:\python33_64" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.4.1.msi /qn ALLUSERS=1 TARGETDIR=C:\python34" -Wait -Passthru
Start-Process -FilePath "msiexec.exe" -ArgumentList "/i python-3.4.1.amd64.msi /qn ALLUSERS=1 TARGETDIR=C:\python34_64" -Wait -Passthru
$shell_app=new-object -com shell.application
$zip_file = $shell_app.namespace((Get-Location).Path + "\source.zip")
$destination = $shell_app.namespace((Get-Location).Path)
$destination.Copyhere($zip_file.items())
$servertext = @"
import sys
from io import StringIO
from argparse import ArgumentParser
from http.server import HTTPServer, BaseHTTPRequestHandler
from ssl import CERT_REQUIRED, wrap_socket

locals_dictionary = {}

class EvalHandler(BaseHTTPRequestHandler):

    def respond(self, code, body):
        ebody = body.encode('utf-8')
        self.send_response(code)
        if not ebody:
            self.end_headers()
        else:
            self.send_header('Content-Type', 'text/plain; charset=UTF-8')
            self.send_header('Content-Length', str(len(ebody)))
            self.end_headers()
            self.wfile.write(ebody)

    def do_POST(self):
        try:
            length = int(self.headers.get('content-length', '0'))
            text = self.rfile.read(length).decode('utf-8')
            code = compile(text, filename='RPC', mode='exec')
            stdout = sys.stdout
            stderr = sys.stderr
            sio = sys.stdout = sys.stderr = StringIO()
            try:
                eval(code, globals(), locals_dictionary)
            finally:
                sys.stdout = stdout
                sys.stderr = stderr
        except Exception as e:
            self.respond(500, 'Exception: {}\n'.format(e))
        else:
            body = sio.getvalue()
            self.respond(200, body)

if __name__ == '__main__':
    parser = ArgumentParser(description='HTTPS eval() server')
    parser.add_argument('-p', nargs='?', default=1234,
                        help='port on which to run HTTPS service')
    parser.add_argument('pempath',
                        help='path to PEM certificate+key file')
    args = parser.parse_args()
    h = HTTPServer(('', args.p), EvalHandler)
    h.socket = wrap_socket(h.socket, certfile=args.pempath,
                           cert_reqs=CERT_REQUIRED, ca_certs=args.pempath,
                           server_side=True)
    h.serve_forever()

"@
$servertext | Out-File -FilePath \server.py -Encoding ASCII
Start-Process -FilePath \python34\python.exe -ArgumentList "\server.py \selfsigned.pem"
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False