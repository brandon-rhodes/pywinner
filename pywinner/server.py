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
