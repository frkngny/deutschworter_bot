import requests


params = {
    'username': 'asd',
    'lang': 'en',
    'a': 'b'
}
resp = requests.post('http://127.0.0.1:5000/api/user/configure', data=params)
