import sys

conversation_file = "data/movie_conversations.txt"
movie_lines_file = "data/movie_lines.txt"
conversation_result_file = "data/conversation_result_file.txt"
encode_file = "data/train.enc"
decode_file = "data/train.dec"

def getLineMap():
  with open(movie_lines_file, "r") as f:
    lines = f.readlines()
  
  lines_map = {}
  for line in lines:
    fields = line.split("+++$+++")
    if len(fields) < 5:
      continue
    lines_map[fields[0].strip()] = fields[4].strip()
  return lines_map

def getConversationLines():
  with open(conversation_file, "r") as f:
    lines = f.readlines()
  
  result = []
  for line in lines:
    fields = line.split("+++$+++")
    if len(fields) < 4:
      continue
    
    result.append([str.strip('[]\n\' ') for str in fields[3].split(',')])
  return result

def writeConversation(lines_map, conversations):
  with open(conversation_result_file, "w") as f:
    for conversation in conversations:
      for line_key in conversation:
        if line_key not in lines_map:
          print("key " + line_key + " does not exist")
          continue
        f.write(lines_map[line_key] + "\n")
      f.write("============++++++++============\n")

def writeData(lines_map, conversations):
  with open(encode_file, "w") as en_f:
    with open(decode_file, "w") as de_f:
      for conversation in conversations:
        for i in range(len(conversation) - 1):
          en_f.write(lines_map[conversation[i]] + "\n")
          de_f.write(lines_map[conversation[i + 1]] + "\n")
  
if __name__ == '__main__':
  mode = sys.argv[1]
  print(mode)
  if mode != "conversation" and mode != "data":
    print("mode: conversation/data")
    exit()
  
  lines_map = getLineMap()
  conversations = getConversationLines()
  
  if mode == "conversation":
    writeConversation(lines_map, conversations)
    exit()
  
  if mode == "data":
    writeData(lines_map, conversations)
    exit()
