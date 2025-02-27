import requests

req =  requests.get("http://127.0.0.1:5000")
print(type(req.text))