#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import tensorflow as tf, sys

PORT_NUMBER = 8080

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("/tf/training/retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("/tf/training/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
sess = tf.Session()
softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		if self.path.endswith(".ico"):
			return
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()

                image_path = "/tf/test/" + self.path;
                print(self.path)
                image_data = tf.gfile.FastGFile(image_path, 'rb').read()
                predictions = sess.run(softmax_tensor, \
                    {'DecodeJpeg/contents:0': image_data})
   
                # Sort to show labels of first prediction in order of confidence
                top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    
                for node_id in top_k:
                   human_string = label_lines[node_id]
                   score = predictions[0][node_id]
                   self.wfile.write('%s (score = %.5f)' % (human_string, score))
                if predictions[0][top_k[0]] > 0.5:
                   self.wfile.write('=============== Hello %s =======================' % (label_lines[top_k[0]]))

		return

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
	
