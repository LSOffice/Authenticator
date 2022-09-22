from http.server import BaseHTTPRequestHandler, HTTPServer
import time, json
from token_generator import TokenRequest
from uuid_generator import UuidRequest
from request_exception import request_failure

hostName = "localhost"
serverPort = 4321
cur_version = "1"

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        http_timeout = json.load(open("data/http_timeout.json", "r+"))
        auth_token = json.load(open("data/auth_token.json", "r+"))
        if self.client_address[0] in http_timeout:
            self.send_response(429)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(request_failure(429, "Too many requests")).encode("utf-8"))
        else:
            args = self.path.split("/")
            args.pop(0)
            if args[0] == "api":
                if args[1] != "v" + cur_version:
                    self.send_response(400)
                    self.send_header("Content-type", "application/json ")
                    self.end_headers()
                    self.wfile.write(
                        json.dumps(
                            request_failure(400, "Invalid api version (outdated/version does not exist)")).encode(
                            "utf-8"))
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json ")
                    self.end_headers()
                    h = {}
                    headers = str(self.headers).splitlines()
                    headers.pop()
                    count = 0
                    for a in headers:
                        h[headers[count][:headers[count].index(":")]] = headers[count][headers[count].index(":") + 2:]
                        count += 1
                    if args[2] == "token":
                        if args[3] == "get":
                            try:
                                tg = TokenRequest({
                                    "uuid": h["uuid"],
                                    "email": h["email"],
                                    "source": h["source"],
                                    "sent": h["sent"]
                                })

                                self.wfile.write(json.dumps(tg.get()).encode("utf-8"))
                            except KeyError as e:
                                self.wfile.write(json.dumps(request_failure(401, "Invalid authorization")).encode("utf-8"))
                    elif args[2] == "uuid":
                        if args[3] == "get":
                            try:
                                ug = UuidRequest({
                                    "email": h["email"],
                                    "source": h["source"],
                                    "sent": h["sent"]
                                })

                                self.wfile.write(json.dumps(ug.get()).encode("utf-8"))
                            except KeyError:
                                self.wfile.write(
                                    json.dumps(request_failure(401, "Invalid authorization")).encode("utf-8"))

                    else:
                        self.wfile.write(json.dumps(request_failure(400, "Bad request")).encode("utf-8"))
            else:
                self.send_response(401)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>Error</title></head>", "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes("<h1>Error 401: Unauthorized access to non-api</h1>", "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), Server)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
