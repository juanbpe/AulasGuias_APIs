import requests
import json


url = 'https://viacep.com.br/ws/59190000/json/'

resposta = requests.get(url)

print(resposta.status_code)

endereco = resposta.json()

print(endereco['localidade'])
print(endereco['uf'])



urlPoke = 'https://pokeapi.co/api/v2/pokemon/charmander'

resposta2 = requests.get(urlPoke)

date = resposta2.json()

# print(json.dumps(date, indent=4))

print(date['abilities'][0]['slot'])