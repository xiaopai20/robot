from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import cv2
import urllib2

PORT_NUMBER = 8080
IMG_PATH = "C:\\Users\\Hannah\\Desktop\\xiaopai\\share_data\\"
RECOGNIZE_SERVICE_URL = "http://192.168.99.100:8088/"

cap = cv2.VideoCapture(0)
curImgIndex = 0

#This class will handles any incoming request from
#the browser
class myHandler(SimpleHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		print "received " + self.path
		if not self.path.endswith("getPersonName"):
			return SimpleHTTPRequestHandler.do_GET(self)



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

		imgFileName = str(curImgIndex) + ".jpg"
		wRet = cv2.imwrite(IMG_PATH + imgFileName, img)
		if not wRet:
			print "saving " + imgFileName + " error"
		print "save " + imgFileName

		personName = urllib2.urlopen(RECOGNIZE_SERVICE_URL + imgFileName).read()
		print personName
		self.wfile.write(personName)

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

