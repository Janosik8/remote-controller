#!/usr/bin/env python3

import RPi.GPIO as GPIO
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep

host_name = '192.168.55.101'  # IP Address of Raspberry Pi
host_port = 5553


def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(2, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)



class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current GPU temperature is {}</p>
           <form action="/" method="POST">
               Turn LED :
               <input type="submit" name="submit" value="Brama">
               <input type="submit" name="submit" value="Garaż">
           </form>
           </body>
           </html>
        '''
        self.do_HEAD()

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]

        setupGPIO()

        if post_data == 'Brama':
            GPIO.output(2, GPIO.HIGH)
            sleep(1)
            GPIO.output(2, GPIO.Low)
        elif post_data == 'Garaż':
            GPIO.output(3, GPIO.HIGH)
            sleep(1)
            GPIO.output(3, GPIO.Low)


        print("LED is {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()