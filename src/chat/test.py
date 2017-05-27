#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys

train_file = "data/legend_of_martial_arts/train.enc"
dic_file = "working_dir_2/vocab20000.enc"

reload(sys).setdefaultencoding('utf-8')

def chinese_tokenizer(sentence):
  sentence = sentence.strip()
  arr = list(unicode(sentence.decode('utf-8', errors='ignore').encode('utf-8')))
  arr = [item.encode('utf-8') for item in arr]
  return arr


rev_vocab = []
with open(dic_file, "rb") as f:
  rev_vocab.extend(f.readlines())
print(rev_vocab[10])
rev_vocab = [(line.strip()) for line in rev_vocab]
vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])

print(rev_vocab)

test_str = ""
with open(train_file, "rb") as f:
  test_str = f.readlines()[0]

print(test_str)
array = chinese_tokenizer(test_str)
print(array)
print vocab["了"]
print vocab[array[0]]