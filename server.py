import asyncio
from urllib.parse import parse_qs
from pathlib import Path
#setting the host and a port
host ='127.0.0.1'
port = 8085

#defining the template folder path ad database file path
TEMPLATE_DIR = Path(__file__).parent/"templates"
DB_FILE = Path(__file__).parent / 'db.txt'#a path to save the registered username  and email

#building http response 
def build_response(status_code, html_content):
   return(
      f"HTTP/1.1 {status_code}\r\n"
      "Content-Type:text/html; charset = utf-8\r\n "
      f"Content-Length: {len(html_content.encode())}\r\n"
      "Connection:close\r\n"
      "\r\n"
      f"{html_content}"
   )

async def handler(reader, writer):
    try: 
        #waiting and read data up 1024 bytes      
        request = await reader.read(1024)
        #decodes bytes into a string and split in individual lines
        request_lines = request.decode().splitlines()
       # closing connetion if data is not recieved

        if not request_lines:
           writer.close()
           await writer.wait_closed()
           return
    
        method, path, _ = request_lines[0].split()

        if method == "GET":       
            if path == "/":
              file_path = TEMPLATE_DIR / "index.html"
            elif path == "/register":
                file_path  = TEMPLATE_DIR/ "register.html"
            else:
                #find a file path by name
                file_path = TEMPLATE_DIR/ path.strip("/")
            if file_path.exists():
                content = file_path.read_text()
                # succesful  response
                response = build_response("200 ok", content)
            else:
               #if file is not found
               not_found =   (TEMPLATE_DIR /"404.html").read_text()            
               response = build_response("404 Not Found ", not_found)
               
        #user submitting the form using post request
        elif method =="POST" and path == "/register":
           body = request.decode().split("\r\n\r\n",1)[1]
           data =parse_qs(body)

           #extracting username from the dictionary
           username = data.get("username", [""])[0]
           email = data.get("email", [""])[0] 

           #append the credentials
           with open(DB_FILE,"a") as f:
              f.write(f"{username} {email}\n")
              
           success_html = "<h1>Registration Successful!</h1><a href='/'>Back to Home</a>"
           response = build_response("200 ok", success_html)

          
        else:
           method_not_allowed = (TEMPLATE_DIR/ "405.html").read_text() 
           response =build_response("405 Method Not Allowed", method_not_allowed)
 
      
        writer.write(response.encode())
        await writer.drain()
  
    except Exception as e:
        print(f"Error handling : {e}")
 
    finally:
      writer.close()
      await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handler, host, port)
    print(f"serving HTTP on {host}:{port}...")
   
    async with server:
      await server.serve_forever()

if __name__ =="__main__":
    asyncio.run(main())                   