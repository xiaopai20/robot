from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from multiprocessing.pool import ThreadPool
import urllib2
import json
import time
import cgi


PORT_NUMBER = 8080
# IMG_PATH = "/Users/pguoping/tensorflow/share_data/"
IMG_PATH = "C:\\Users\\Hannah\\Desktop\\xiaopai\\share_data"
HUMAN_RECOGNIZE_SERVICE_URL = "http://192.168.99.100:8088/"
BASIC_RECOGNIZE_SERVICE_URL = "http://192.168.99.100:8089/"

CAMERA_CALLBACK_URL = "http://192.168.1.147:8080/get"
SPEAK_CALLBACK_URL = "http://192.168.1.147:8080/speak?"

pool = ThreadPool(processes=2)
curImgIndex = 0


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

	def do_POST(self):
		startTime = time.time()
		print "received " + self.path
		if not self.path.endswith("parse"):
			return SimpleHTTPRequestHandler.do_GET(self)

		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()

		global curImgIndex
		curImgIndex += 1
		curImgIndex %= 100

		imgFileName = str(curImgIndex) + ".jpg"

		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					 'CONTENT_TYPE':self.headers['Content-Type'],
					 })
		filename = form['file'].filename
		file_content = form['file'].file.read()

		with open(IMG_PATH + imgFileName, 'wb') as fh:
			fh.write(file_content)
			print "write file " + imgFileName

		#personAsyncCall = pool.apply_async(callUrl, (HUMAN_RECOGNIZE_SERVICE_URL + imgFileName,))
		#itemAsyncCall = pool.apply_async(callUrl, (BASIC_RECOGNIZE_SERVICE_URL + imgFileName,))

		#personName = personAsyncCall.get(1000)
		#itemName = itemAsyncCall.get(1000)

		personName = callUrl(HUMAN_RECOGNIZE_SERVICE_URL + imgFileName)
		itemName = callUrl(BASIC_RECOGNIZE_SERVICE_URL + imgFileName)

		ret = {'image' : imgFileName,
			   'person' : personName,
			   'item' : itemName,
			   'delay' : int(1000 * (time.time() - startTime))}
		print ret
		self.wfile.write(json.dumps(ret))

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

