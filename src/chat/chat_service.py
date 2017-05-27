#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import tensorflow as tf, sys
import chat
import data_utils
import time
import urllib.parse
import os
import numpy as np

PORT_NUMBER = 8085

_buckets = [(5, 10), (10, 15), (20, 25), (40, 50)]

sess = tf.Session()

chat.gConfig = chat.get_config("seq2seq_2.ini")

# Create model and load parameters.
model = chat.create_model(sess, True)
model.batch_size = 1  # We decode one sentence at a time.

# Load vocabularies.
enc_vocab_path = os.path.join(chat.gConfig['working_directory'],"vocab%d.enc" % chat.gConfig['enc_vocab_size'])
dec_vocab_path = os.path.join(chat.gConfig['working_directory'],"vocab%d.dec" % chat.gConfig['dec_vocab_size'])

enc_vocab, _ = data_utils.initialize_vocabulary(enc_vocab_path)
_, rev_dec_vocab = data_utils.initialize_vocabulary(dec_vocab_path)

def chinese_tokenizer(sentence):
  sentence = sentence.strip()
  print(sentence.encode('utf-8'))
  arr = [c for c in sentence]
  return arr


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
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        
        urlSegments = self.path.split("?")
        if len(urlSegments) < 2:
          self.wfile.write("Invalid request")
          return

        sentence = urllib.parse.unquote(urlSegments[1])
        print("received: ".encode('utf-8') + sentence.encode('utf-8'))
        # Get token-ids for the input sentence.
        token_ids = data_utils.sentence_to_token_ids(sentence, enc_vocab, chinese_tokenizer, False)
        print(token_ids)
        # Which bucket does it belong to?
        bucket_id = min([b for b in range(len(_buckets))
                         if _buckets[b][0] > len(token_ids)])
        # Get a 1-element batch to feed the sentence to the model.
        encoder_inputs, decoder_inputs, target_weights = model.get_batch(
            {bucket_id: [(token_ids, [])]}, bucket_id)
        # Get output logits for the sentence.
        _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
                                         target_weights, bucket_id, True)
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
        # If there is an EOS symbol in outputs, cut them at that point.
        if data_utils.EOS_ID in outputs:
          outputs = outputs[:outputs.index(data_utils.EOS_ID)]
        # Print out French sentence corresponding to outputs.
        output_text = "".join([tf.compat.as_str(rev_dec_vocab[output]) for output in outputs])

        self.wfile.write(output_text.encode('utf-8'))
        print(output_text.encode('utf-8'))
        print("delay: " + str(time.time() - startTime))

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
