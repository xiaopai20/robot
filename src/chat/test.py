#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib.parse

t = u"这是一个句子"
arr = [c for c in t]
print(arr[0].encode('utf-8'))
print(arr[2].encode('utf-8'))

text = "%E6%88%91%E9%9D%A0"
text = urllib.parse.unquote(text)
print("received: ".encode('utf-8') + text.encode('utf-8'))
