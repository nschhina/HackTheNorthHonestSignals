from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import random
import wav_file_analysis
import scipy.io.wavfile as sc

class S(BaseHTTPRequestHandler):
    def _set_headers(self, code=200, content_type='text/html'):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        relative_path = self.path[1:]
        if not relative_path:
            relative_path = "index.html"
        print("Serving " + relative_path)
        if os.path.isfile(relative_path):
            content_type = 'text/html'
            if relative_path.endswith(".css"):
                content_type = 'text/css'
            self._set_headers(200, content_type)
            f = open(relative_path, "rb")
            self.wfile.write(f.read())
        else:
            self._set_headers(404)
            self.wfile.write("File %s not found" % relative_path)


    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        wav_file_analysis.wav_analysis(sc.read(self.data_string))
        print("File uploaded: " + self.headers['Content-Length'])

        self.send_response(200)
        self.end_headers()

        # data = simplejson.loads(self.data_string)
        self.wfile.write("OK: " + self.headers['Content-Length'])
        return


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
