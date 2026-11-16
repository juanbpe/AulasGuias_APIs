# 1. Liste todas as tarefas (/todos) do usuário de userId 2 e mostre quantas estão concluídas ("completed": true).
# 2. Busque o usuário de id 3 (/users/3) e exiba seu nome, e-mail e cidade (dica: a cidade fica em address → city).
# 3. Liste os comentários do post de id 5 (/posts/5/comments) mostrando o e-mail de quem comentou.
# EXTRA. Desafio: escolha um endpoint e crie um menu no terminal (1 - Listar, 2 - Buscar, 3 - Criar, 4 - Atualizar, 5 - Excluir, 0 - Sair). Dica: usar função.

import requests

URL = 'https://jsonplaceholder.typicode.com'

# ============================================ #
#      1. Tarefa do usuário de userId 2
# ============================================ #

resposta = requests.get(URL + "/todos?userId=2")
tarefas = resposta.json()

print("Status: ", resposta.status_code)
print("\nTarefas do usuário 2:")

concluidas = 0

for tarefa in tarefas:
    print(tarefa['id'], " - ", tarefa['title'], " - Concluída:", tarefa['completed'])

    if tarefa['completed'] == True:
        concluidas += 1

print("\nTotal de tarefas concluídas: ", concluidas)


# ============================================ #
#        2. Busca do usuário de id 3
# ============================================ #

resposta_2 = requests.get(URL + "/users/3")
usuario = resposta_2.json()

print("\nStatus: ", resposta_2.status_code)
print("Nome: ", usuario["name"])
print("E-mail: ", usuario["email"])
print("Cidade: ", usuario["address"]["city"])


# ============================================ #
#          3. Lista de comentários
# ============================================ #

resposta_3 = requests.get(URL + "/posts/5/comments")
comentarios = resposta_3.json()

print("\nStatus: ", resposta_3.status_code)
print("\nE-mails dos comentários do post 5:")

for comentario in comentarios:
    print(comentario["email"])