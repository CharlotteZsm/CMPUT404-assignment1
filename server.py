#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        info = self.data.decode("utf-8").split()
        method, address, self.version = info[0], info[1], info[2]

        #Check if the method is GET. If not, send 405 Error.
        if method != "GET":
            response = self.Error405()
        else:
            url = "www"+address
            if address[-1] == "/":
                url += "index.html"
                response = self.OK200("html", url)
            else:
                url_split = url.split('.')
                if len(url_split) == 1:
                    path = address+"/"
                    url += "/index.html"
                    response = self.Error301(url,path)
                elif len(url_split) == 2:
                    type = url_split[1]
                    if (type !='css' and type != 'html'):
                        response = self.Error404()
                    else:
                        response = self.OK200(type, url)
                else:
                    response = self.Error404()
        print(response)
        self.request.sendall(bytearray(response,'utf-8'))

    def Error405(self):
        response = self.version+" 405 Method Not Allowed\r\n"+"Content-Type: text/html\n"
        return response
    def Error404(self):
        response = self.version+" 404 Not Found\r\n"+"Content-Type: text/html\n"
        return response
    def Error301(self,url,path):
        content = self.Get_content(url)
        if content == None:
            response = self.Error404()
            return response
        response = self.version+" 301 Moved Permanently\r\n"+"Content-Type: text/html\n"+"Location: "+path+"\n"+content
        return response
    def OK200(self,type,url):
        content = self.Get_content(url)
        if content == None:
            response = self.Error404()
            return response
        response = self.version+" 200 OK\r\n"+"Content-Type: text/"+type+"\r\n\n"+content
        return response
    def Get_content(self, url):
        try:
            f = open(url, "r")
        except:
            return None
        content = f.read()
        f.close()
        return content
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
