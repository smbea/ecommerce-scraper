from http.server import BaseHTTPRequestHandler
from scrapper import scrapeUrl
from urllib.parse import urlparse, parse_qs
import json
class Server(BaseHTTPRequestHandler):
  def do_HEAD(self):
    return
    
  def do_GET(self):
    self.respond()
    
  def do_POST(self):
    return
    
  def handle_http(self, status, content_type):
    self.send_response(status)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    parsed = urlparse(self.path)

    print("request path: " + self.path)


    try:
      url = parse_qs(parsed.query)['url'][0]
    except:
      return "Can not read url"
    
    try:
      info = scrapeUrl(url)
      return json.dumps(info)
    except:
      return "Error"

    
  def respond(self):
    content = self.handle_http(200, 'application/json')
    self.wfile.write(bytes(content, "UTF-8"))

    