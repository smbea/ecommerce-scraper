#!/usr/bin/env python3
import time
from http.server import HTTPServer
from server import Server
from scrapper import init_driver

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000

if __name__ == '__main__':
    
    driver = init_driver()

    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    driver.quit()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))