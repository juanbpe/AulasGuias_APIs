import requests

URL = 'https://dummyjson.com/auth'

headers = {
    'Content-Type': 'application/json'
}

credenciais = {
    'username': 'emilys',
    'password': 'emilyspass',
    'expiresInMins': 30,
}


resposta = requests.post(URL+"/login", headers=headers, json=credenciais)

print(resposta.status_code)
print(resposta.json()['accessToken'])

token = resposta.json()['accessToken']

# Acesso NÃO autorizado
resposta_2 = requests.get(URL+"/me")
print(resposta_2.status_code)
print(resposta_2.json())

# Acesso autorizado
headers_2 = {
    'Authorization': 'Bearer '+token
  }

resposta_3 = requests.get(URL+"/me", headers=headers_2)
print(resposta_3.status_code)
print(resposta_3.json())

# Atualização de Token
dados = {
    'refreshToken': token,
    'expiresInMins': 30,
}

resposta_4 = requests.post(URL+"/refresh", headers=headers_2, json=dados)
print(resposta_4.status_code)
print(resposta_4.json())