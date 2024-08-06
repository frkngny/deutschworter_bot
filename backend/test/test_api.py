import requests


params = {
    'username': 'asd',
    'lang': 'en',
    'a': 'b'
}
resp = requests.get('http://127.0.0.1:5000/api/get_word', data=params)
print(resp.json())
