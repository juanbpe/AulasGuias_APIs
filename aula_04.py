import requests


url = 'http://127.0.0.1:8000/api/v1/materias/'

resposta = requests.get(url)

print(resposta.status_code)

lista_materias = resposta.json()

print(lista_materias[0]['nome'])   