import requests

data = {"amount": 1, "item":5, "user": 1}
url = 'http://127.0.0.1:8000/api/reduce-item'

r = requests.post(url, data=data).json()

print(r)
