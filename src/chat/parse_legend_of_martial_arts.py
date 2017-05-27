#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys

conversation_file = "data/legend_of_martial_arts/all.txt"
trimmed_conversation_file = "data/legend_of_martial_arts/trimmed.txt"
noname_conversation_file = "data/legend_of_martial_arts/noname.txt"
train_enc_file = "data/legend_of_martial_arts/train.enc"
train_dec_file = "data/legend_of_martial_arts/train.dec"

name_mapping = {
  "李大嘴" : "李大嘴",
  "嘴" : "李大嘴",
  "李" : "李大嘴",
  "大嘴" : "李大嘴",
  
  "莫小贝" : "莫小贝",
  "小贝" : "莫小贝",
  "贝" : "莫小贝",
  
  "掌柜" : "佟掌柜",
  "湘玉" : "佟掌柜",
  "佟湘玉" : "佟掌柜",
  "佟" : "佟掌柜",
  "掌柜的" : "佟掌柜",
  
  "白展堂" : "白展堂",
  "老白" : "白展堂",
  "展堂" : "白展堂",
  "白" : "白展堂",
  
  "无双" : "无双",
  "双" : "无双",
  "祝无双" : "无双",
  
  "小郭" : "郭芙蓉",
  "郭" : "郭芙蓉",
  "郭芙蓉" : "郭芙蓉",
  
  "吕" : "吕秀才",
  "吕秀才" : "吕秀才",
  "秀才" : "吕秀才",
  "吕轻侯" : "吕秀才",
  
  "老邢" : "老邢",
  "刑捕头" : "老邢",
  "邢" : "老邢",
  
  "小六" : "小六",
  "燕小六" : "小六",
  "六" : "小六"
}

def getName(name_str):
  name = name_str.strip()
  name = name.strip("　")
  name = name.split("（")[0]
  name = name.strip()
  name = name.strip("　")
  
  ret = name in name_mapping
  if ret:
    name = name_mapping[name]
  return ret, name

def parseLine(text):
  text = text.strip().strip("　")
  rightIndex = text.replace("“", "")
  rightIndex = text.replace("”", "")
  leftIndex = text.find("（")
  rightIndex = text.find("）")
  while leftIndex != -1 and rightIndex != -1 and rightIndex > leftIndex:
    text = text[:leftIndex] + text[rightIndex + 3:]
    leftIndex = text.find("（")
    rightIndex = text.find("）")
  
  lines = text.split("。")
  if not lines[-1]:
    del lines[-1]
    if len(lines) > 0:
      lines[-1] += "。"
  
  for i in range(len(lines) - 1):
    lines[i] += "。"
  
  return lines

with open(conversation_file, "r") as f:
  lines = f.readlines()

new_lines = []
for line in lines:
  fields = line.split("：")
  if len(fields) != 2:
    continue
  
  # ret, name = getName(fields[0])
  # if not ret:
  #   continue
  
  new_lines.extend(parseLine(fields[1]))
  
with open(noname_conversation_file, "w") as f:
  for line in new_lines:
    f.write(line + "\n")


with open(train_enc_file, "w") as enc_f:
  with open(train_dec_file, "w") as dec_f:
    for i in range(len(new_lines) - 1):
      enc_f.write(new_lines[i] + "\n")
      dec_f.write(new_lines[i+1] + "\n")
    