class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers

    def balance(self):
        server_index = len(self.servers) % len(self.servers)
        return self.servers[server_index]

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        server = load_balancer.balance()
        conn = http.client.HTTPConnection(server)
        conn.request("GET", self.path)
        response = conn.getresponse()
        
        self.send_response(response.status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.read())
        conn.close()

if __name__ == "__main__":
    servers = ["localhost:8000", "localhost:8001", "localhost:8002"]
    load_balancer = LoadBalancer(servers)

    server_address = ("", 8080)
    httpd = http.server.HTTPServer(server_address, HTTPRequestHandler)
    print("Load Balancer running at port 8080")
    httpd.serve_forever()
