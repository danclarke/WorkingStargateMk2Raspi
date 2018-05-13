import os
import json
from SimpleHTTPServer import SimpleHTTPRequestHandler

# Useful stuff from: https://stackoverflow.com/a/46332163


class StargateHttpHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join('web', relpath)
        return fullpath

    def do_POST(self):
        print('POST: {}'.format(self.path))
        if self.path != '/update':
            self.send_error(404)
            return

        content_len = int(self.headers.getheader('content-length', 0))
        body = self.rfile.read(content_len)
        data = json.loads(body)
        StargateHttpHandler.logic.execute_command(data)
        self.send_response(200, 'OK')
