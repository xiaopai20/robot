from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from multiprocessing.pool import ThreadPool
import cv2
import urllib2
import json
import time
import requests
import pyttsx


PORT_NUMBER = 8080
IMG_PATH = "C:\\robot\\capture\\"
SERVICE_URL_PARSE_IMG = "http://192.168.137.72:8080/parse"

cap = cv2.VideoCapture(0)
curImgIndex = 0

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')

def callUrl(url):
	return urllib2.urlopen(url, timeout=1000).read()

#This class will handles any incoming request from
#the browser
class myHandler(SimpleHTTPRequestHandler):

	def speak(self):
		engine.say(self.path.split("?")[1])
		engine.runAndWait()

	#Handler for the GET requests
	def do_GET(self):
		if self.path.startswith("/speak"):
			self.speak()
			return

		if not self.path.endswith("get"):
			return SimpleHTTPRequestHandler.do_GET(self)
		startTime = time.time()
		print "received " + self.path

		self.send_response(200)
		self.send_header('cache-control','max-age=0')
		self.send_header('cache-control','no-cache')
		self.send_header('Content-type','text/html')
		self.end_headers()

		# double read to capture latest pic,
		# other wise it will return last 2nd one, don't know why...
		cap.read()
		ret, img = cap.read()
		if not ret:
			self.wfile.write("Capture image error")
			return

		#cv2.imshow("input", img)
		global curImgIndex
		curImgIndex += 1
		curImgIndex %= 100

		imgFilePath = IMG_PATH + str(curImgIndex) + ".jpg"
		wRet = cv2.imwrite(imgFilePath, img)
		if not wRet:
			print "saving " + imgFilePath + " error"
		print "save " + imgFilePath

		file_ = {'file': open(imgFilePath, 'rb')}
		r = requests.post(SERVICE_URL_PARSE_IMG, files=file_)
		print r.text
		self.wfile.write(r.text)

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

