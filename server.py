import os
from http.server import SimpleHTTPRequestHandler, HTTPServer, BaseHTTPRequestHandler
import cgi
import base64
import json

UPLOAD_DIR = 'uploads'
USERNAME = 'admin'
PASSWORD = 'password'

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class MyHandler(BaseHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Login Required"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None:
            self.do_AUTHHEAD()
            self.wfile.write(b'Authentication required.')
        else:
            auth_type, auth_data = auth_header.split()
            if auth_type.lower() == 'basic':
                auth_data = base64.b64decode(auth_data).decode('utf-8')
                username, password = auth_data.split(':')
                if username == USERNAME and password == PASSWORD:
                    self.handle_request()
                else:
                    self.do_AUTHHEAD()
                    self.wfile.write(b'Invalid credentials.')
    
    def handle_request(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Hello, World! This is the home page.")
        elif self.path == '/about':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"About Page")
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = {'key': 'value', 'number': 42}
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif self.path == '/upload':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body>
                <form enctype="multipart/form-data" method="post">
                    <input type="file" name="file"><br>
                    <input type="submit" value="Upload">
                </form>
                </body>
                </html>
            """)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Page not found!")
    
    def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers['content-type'])
        if content_type == 'multipart/form-data':
            fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            if 'file' in fs:
                file_item = fs['file']
                if file_item.filename:
                    file_path = os.path.join(UPLOAD_DIR, os.path.basename(file_item.filename))
                    with open(file_path, 'wb') as f:
                        f.write(file_item.file.read())
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"File uploaded successfully!")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"No file uploaded.")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No file uploaded.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid content type.")

    def log_message(self, format, *args):
        with open("server.log", "a") as log_file:
            log_file.write(f"{self.address_string()} - - [{self.log_date_time_string()}] {format % args}\n")

PORT = 8000

with HTTPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
