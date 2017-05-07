from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from multiprocessing.pool import ThreadPool
import urllib2
import json
import time
import cgi


PORT_NUMBER = 8080
CAMERA_CALLBACK_URL = "http://192.168.1.147:8080/get"
SPEAK_CALLBACK_URL = "http://192.168.1.147:8080/speak?"

def callUrl(url):
	return urllib2.urlopen(url, timeout=3000).read()

#This class will handles any incoming request from
#the browser
class myHandler(SimpleHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		print "received " + self.path
		if self.path.endswith("get"):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write(callUrl(CAMERA_CALLBACK_URL))
			return

		if self.path.startswith("/speak"):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write(callUrl(SPEAK_CALLBACK_URL + self.path.split("?")[1]))
			return

		return SimpleHTTPRequestHandler.do_GET(self)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()

