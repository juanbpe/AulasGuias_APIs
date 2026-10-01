import requests

URL = "https://jsonplaceholder.typicode.com"
resposta = requests.get(URL+"/posts")
posts = resposta.json()


print("Status: ", resposta.status_code)
print(posts)
print("Total de posts:", len(posts))

# Mostra todos os títulos
for cesar in posts:
    print(cesar['id']," - ",cesar['title'])

# Mostra só os 3 primeiros títulos
for cesar in posts[:3]:
    print(cesar['id']," - ",cesar['title'])

# =========================================================== #

resposta_2 = requests.get(URL+"/posts/1")
posts_2 = resposta_2.json()

print("Status:", resposta.status_code)
print("Título:", posts_2["title"])
print("Conteúdo:", posts_2["body"])

# =========================================================== #

novo_post = {
    'userId': 1,
    'title': 'Aula de API',
    'body': 'Aula de BG',
}

resposta_3 = requests.post(URL+"/posts", json=novo_post)

print(resposta_3.status_code)

retorno = resposta_3.json()

print(retorno)

# =========================================================== #

post_alterado = {
    'userId': 1,
    'title': 'API é importante',
    'body': 'Agora eu sei API',
}

resposta_4 = requests.put(URL+"/posts/1", json=post_alterado)

print(resposta_4.status_code)
print(resposta_4.json())

# =========================================================== #

resposta_5 = requests.delete(URL+"/posts/2")

print(resposta_5.status_code)
print(resposta_5.json())