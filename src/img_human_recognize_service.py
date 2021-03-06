#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import tensorflow as tf, sys
import time

PORT_NUMBER = 8088
IMAGE_ROOT = "C:\\Users\\Hannah\\Desktop\\xiaopai\\share_data\\"
RETRAINED_TXT = "C:\\Users\\Hannah\\Desktop\\xiaopai\\training\\retrained_labels.txt"
RETRAINED_GRAPH = "C:\\Users\\Hannah\\Desktop\\xiaopai\\training\\retrained_graph.pb"

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile(RETRAINED_TXT)]

# Unpersists graph from file
with tf.gfile.FastGFile(RETRAINED_GRAPH, 'rb') as f:
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
        print("receive: " + self.path)
        startTime = time.time()
        if self.path.endswith(".ico"):
            return
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        image_path = IMAGE_ROOT + self.path
        print(self.path)
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
        predictions = sess.run(softmax_tensor, \
            {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
           human_string = label_lines[node_id]
           score = predictions[0][node_id]
           print('%s (score = %.5f)' % (human_string, score))
        if predictions[0][top_k[0]] > 0.5:
           self.wfile.write(label_lines[top_k[0]].encode())

        print("delay: " + str(time.time() - startTime) + " " + label_lines[top_k[0]])

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ' , PORT_NUMBER)

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()

