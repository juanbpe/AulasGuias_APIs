# import requests

# URL = 'http://127.0.0.1:8000/api/'

# r = requests.post(URL + 'areas/', json={'nome': 'Qualquer coisa'})
# print(r.status_code)
# requests.delete(URL + f"area_cadastrar/{r.json()['id']}/")

import requests

URL = 'http://127.0.0.1:8000/api/v1/'

r = requests.get(URL + 'areas/')
print(r.json())

r = requests.post(URL + 'area_cadastrar/', json={'nome': 'Eventos'})
print("\n", r.status_code)