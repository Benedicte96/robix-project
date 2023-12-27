import requests

# Effectuer la requête GET à l'API
response = requests.get('http://127.0.0.1:5000/api/robot-host')
data = response.json()
print(data['robotHost'])
print(data['param'])