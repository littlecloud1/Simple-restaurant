from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi


restaurant_form = '''
                        <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                        <h2>Make a new restaurant</h2>
                        <input name="newRestaurantName" type="text" 
                        placeholder="New Restaurant Name" >
                        <input type="submit" value="Create"> </form>
                '''  


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            #connect to database
            engine = create_engine('sqlite:///restaurantmenu.db')
            Base.metadata.bind=engine
            DBSession = sessionmaker(bind = engine)
            session = DBSession()
            
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
             
                msg = ""
                msg += restaurant_form
                msg +="</body></html>"
                self.wfile.write(msg.encode())
                return   
            
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                msg = ""
                items = session.query(Restaurant).all()
                for i in items:
                    msg += i.name + '<br>'
                    msg += '<a href="/restaurants/' + str(i.id) + '/edit">edit</a><br>'
                    msg += '<a href="/restaurants/' + str(i.id) + '/delete">delete</a><br><br>'
                msg +="</body></html>"
                self.wfile.write(msg.encode())
                return   
                
            if self.path.endswith("/edit"):
                #retreive id from database
                rest_id = self.path.split('/')[2]
                
                if rest_id == "":
                    self.send_error(404, 'wrong ID')
                item = session.query(Restaurant).filter_by(id = rest_id)[0]
                
                
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                edit_form = ""
                edit_form += "<form method='POST' enctype='multipart/form-data'"
                edit_form += "action='/restaurants/{}/edit'>".format(item.id)
                edit_form += '<h2>{}</h2>'.format(item.name)
                edit_form += "<input name='newRestaurantName' type='text'"
                edit_form += "placeholder='{}' >".format(item.name)
                edit_form += "<input type='submit' value='Rename'> </form>"
                edit_form += "</body></html>"
                
                self.wfile.write(edit_form.encode())
                return
                
            if self.path.endswith("/delete"):
                #retreive id from database
                rest_id = self.path.split('/')[2]
                
                if rest_id == "":
                    self.send_error(404, 'wrong ID')
                item = session.query(Restaurant).filter_by(id = rest_id)[0]
                
                
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                edit_form = ""
                edit_form += "<form method='POST' enctype='multipart/form-data'"
                edit_form += "action='/restaurants/{}/delete'>".format(item.id)
                edit_form += '<h2>Are you sure you want to delete {}?</h2>'.format(item.name)
                edit_form += "<input type='submit' value='Delete'> </form>"
                edit_form += "</body></html>"
                
                self.wfile.write(edit_form.encode())
                return
                
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
        
        except:
            raise

    def do_POST(self):
        try:
            #connect to database
            engine = create_engine('sqlite:///restaurantmenu.db')
            Base.metadata.bind=engine
            DBSession = sessionmaker(bind = engine)
            session = DBSession()
            
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers['content-type'])

                # boundary data needs to be encoded in a binary format
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                
                    newRestaurant = Restaurant(name = messagecontent[0].decode())
                    
                    session.add(newRestaurant)
                    session.commit()
                    output = ""
                    output += "<html><body>"
                    output += " <h2> Okay, A new Restaurant added : </h2>"
                    output += "<h1> %s </h1>" % messagecontent[0].decode()
                    output += restaurant_form
                    output += "<a href='/restaurants'>Back</a>"
                    output += "</body></html>"
                    
                    self.wfile.write(output.encode())
                    return
                
            if self.path.endswith("/edit"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers['content-type'])

                # boundary data needs to be encoded in a binary format
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    rest_id = self.path.split('/')[2]
                    item = session.query(Restaurant).filter_by(id = rest_id)[0]
                    oldname = item.name
                    item.name = messagecontent[0].decode()
                    
                    session.add(item)
                    session.commit()
                    
                    output = ""
                    output += "<html><body>"
                    output += " <h2> Okay, {} renamed as: </h2>".format(oldname)
                    output += "<h1> %s </h1>" % messagecontent[0].decode()
                    output += "<form method='POST' enctype='multipart/form-data'"
                    output += "action='/restaurants/{}/edit'>".format(item.id)
                    output += "<input name='newRestaurantName' type='text'"
                    output += "placeholder='{}' >".format(item.name)
                    output += "<input type='submit' value='Rename'> </form>"
                    output += "<a href='/restaurants'>Back</a>"
                    output += "</body></html>"
                    
                    self.wfile.write(output.encode())
                    return
                    
                    
            if self.path.endswith("/delete"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                rest_id = self.path.split('/')[2]
                item = session.query(Restaurant).filter_by(id = rest_id)[0]
                name = item.name
                
                session.delete(item)
                session.commit()
                
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, {} has been deleted. </h2>".format(name)
                output += "<a href='/restaurants'>Back</a>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                return
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