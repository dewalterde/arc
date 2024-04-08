import http.server
import socketserver
import socket

# Kullanıcıdan port numarasını al
try:
    PORT = int(input("Enter the port number (e.g., 4000): "))
except ValueError:
    print("Invalid port number. Defaulting to 4000.")
    PORT = 4000

# Local IP adresini al
def get_local_ip():
    try:
        # Socket oluştur
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error as e:
        print(f"Error getting local IP: {e}")
        return "127.0.0.1"  # Default olarak loopback IP kullan

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/'  # Default olarak gönderilecek dosya
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyHttpRequestHandler

try:
    local_ip = get_local_ip()
    with socketserver.TCPServer((local_ip, PORT), Handler) as httpd:
        print(f"Serving at http://{local_ip}:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
except Exception as e:
    print(f"Error: {e}")
