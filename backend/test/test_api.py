import requests


params = {
    'username': 'testuser'
}
json = requests.get('http://127.0.0.1:5000/api/get_word', data=params)
print(json.json())