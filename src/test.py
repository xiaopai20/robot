import requests


file_ = {'file': open('C:/Users/Hannah/Desktop/xiaopai/test/4.jpg', 'rb')}

r = requests.post("http://localhost:8080/parse", files=file_)

print r.text