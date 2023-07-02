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
    parsed = urlparse(self.path)

    if not parsed.query:
      return 200, json.dumps({"message": "Hello World"})

    url = parse_qs(parsed.query)['url'][0]

    if not isValidUrl(url):
      return 400, json.dumps({"message": "Invalid url"})
    
    try:
      info = scrapeUrl(url)
      if info == "Not supported yet":
        return 501, json.dumps({"message": "Website not supported yet"})
      elif info == "Timed out waiting for page to load":
        return 500, json.dumps({"message": "Timed out waiting for page to load"})
      else:
        return 200, json.dumps(info)
    except:
      return 500, json.dumps({"message": "Unknown error occured"})
    
  def handle_health(self):
    return 200, json.dumps({"message": "OK"})

    
  def respond(self):
    parsedUrl = urlparse(self.path)
    path = parsedUrl.path

    if path == '/health':
      status, content = self.handle_health()
    else:
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