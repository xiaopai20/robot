import requests


file_ = {'file': open('C:/Users/Hannah/Desktop/xiaopai/share_data/4.jpg', 'rb')}

r = requests.post("http://192.168.137.72:8081/parse", files=file_)

print r.text