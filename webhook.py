from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class WebHook(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
	print json.dumps(json.loads(self.rfile.read(int(self.headers.getheader('content-length')))), indent=4)

server = HTTPServer(('0.0.0.0', 8000), WebHook)
server.serve_forever()
