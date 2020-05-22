import sys
import os.path
import uuid
from glob import glob
from datetime import datetime

class HttpServer:
    # constructor
    def __init__(self):
        self.sessions = {}
        self.types = {}
        # defining types of files
        self.types['.pdf']  = 'application/pdf'
        self.types['.jpg']  = 'image/jpg'
        self.types['.txt']  = 'text/plain'
        self.types['.html'] = 'text/html'
        self.types['.ico']  = 'image/icon'

    def response(self, code=404, message='Not Found', messageBody=bytes(), headers={}):
        date = datetime.now().strftime('%c')
        resp = []

        resp.append('HTTP/1.0 {} {}\r\n'.format(code, message))
        resp.append('Date: {}\r\n'.format(date))
        resp.append('Connection: close\r\n')
        resp.append('Server: myserver/1.0\r\n')
        resp.append('Content-Length: {}\r\n'.format( len(messageBody) ))

        for header in headers:
            resp.append('{}:{}\r\n'.format(header, headers[header]))
        resp.append('\r\n')

        response_headers = ''
        for respond in resp:
            response_headers = "{}{}".format(response_headers, respond)
        
        if type(messageBody) is not bytes:
            messageBody = messageBody.encode()
        
        response = response_headers.encode() + messageBody
        return response

    def process(self, data):
        requests = data.split('\r\n')
        line = requests[0]
        allHeaders = [ n for n in requests[1:] if n != '' ]
        j = line.split(' ')
        
        try:
            method = j[0].upper().strip()
            if method == 'GET':
                object_address = j[1].strip()
                return self.http_get(object_address, allHeaders)
            else:
                return self.response(400, 'Bad Request', '', {})
        except IndexError:
            return self.response(400, 'Bad Request', '', {})

    def http_get(self, object_address, headers):
        files = glob('./*')
        thisDirectory = '.'
        if thisDirectory + object_address not in files:
            return self.response(404, 'Not Found', '', {})

        fp = open(thisDirectory + object_address, 'rb')
        content = fp.read()
        fextension = os.path.splitext(thisDirectory + object_address)[1]
        content_type = self.types[fextension]

        headers = {}
        headers['Content-type'] = content_type
        return self.response(200, 'OK', content, headers)

if __name__ == "__main__":
    httpserver = HttpServer()
    msg = httpserver.process('GET test.html HTTP/1.0')
    print(msg.decode())