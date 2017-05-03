from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import sys, getopt, datetime
import cv2

PORT_NUMBER = 8080
IMG_PATH = "C:\\Users\\Hannah\\Desktop\\xiaopai\\share_data\\"

cap = cv2.VideoCapture(0)
curImgIndex = 1;

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
	    if not self.path.endswith(".ico"):
		    return

		self.send_response(200)
		self.send_header('Content-type','text')
		self.end_headers()

		ret, img = cap.read();
		if not ret:
		    self.wfile.write("Capture image error")
		    return
		cv2.imwrite(IMG_PATH + curImgIndex + ".jpg", img)
		curImgIndex += 1
		curImgIndex %= 100

		self.wfile.write(IMG_PATH + curImgIndex + ".jpg")

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

