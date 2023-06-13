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
    
  def handle_http(self):
    print("request path: " + self.path)

    parsed = urlparse(self.path)
    url = parse_qs(parsed.query)['url'][0]

    if not isValidUrl(url):
      return 400, json.dumps({"message": "Invalid url"})
    
    try:
      info = scrapeUrl(url)
      if info == "Not supported yet":
        return 404, json.dumps({"message": "Website not supported yet"})
      return 200, json.dumps(info)
    except:
      return 500, json.dumps({"message": "Unknown error occured"})

    
  def respond(self):
    status, content = self.handle_http()
    self.send_response(status)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(bytes(content, "UTF-8"))

    
def isValidUrl(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except:
    return False