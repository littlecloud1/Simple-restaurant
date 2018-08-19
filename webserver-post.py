from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                msg = ""
                msg += "<h1>Hello!</h1>"
                msg += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                msg +="</body></html>"
                self.wfile.write(msg.encode())
                return
                
                
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                msg = ""
                msg += "<h1>&#161 Hola !</h1>"
                msg += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                msg +="</body></html>"
                
                self.wfile.write(msg.encode())
                return
                
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            print(ctype)
            print(pdict)
            # boundary data needs to be encoded in a binary format
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                print("Fields value is", fields)
                messagecontent = fields.get('message')
                
            print(messagecontent)
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0].decode()
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            
            self.wfile.write(output.encode())
            print(output)
            
        except:
            raise
            

def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webServerHandler)
        print ("Web Server running on port %s"%port)
        server.serve_forever()
        
    
    except KeyboardInterrupt:
        print("^C entered, stopping web server..")
        server.socket.close()
        
if __name__ == '__main__':
    main()