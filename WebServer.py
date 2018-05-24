import os
import json
from SimpleHTTPServer import SimpleHTTPRequestHandler
from DialProgram import DialProgram

# Useful stuff from: https://stackoverflow.com/a/46332163


class StargateHttpHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join('web', relpath)
        return fullpath

    def do_POST(self):
        print('POST: {}'.format(self.path))

        if self.path == '/shutdown':
            os.system('systemctl poweroff')
            self.send_response(200, 'OK')
            return

        if self.path == '/dialstatus':
            if DialProgram.is_dialing:
                self.send_response(200, '1')
            else:
                self.send_response(204, '0')
            return

        if self.path != '/update':
            self.send_error(404)
            return

        content_len = int(self.headers.getheader('content-length', 0))
        body = self.rfile.read(content_len)
        data = json.loads(body)
        StargateHttpHandler.logic.execute_command(data)
        self.send_response(200, 'OK')
