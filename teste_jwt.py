# Dicas:
# Aqui não precisa de requests.Session(): não tem cookie para guardar.
# O cabeçalho: headers={'Authorization': 'Bearer ' + access} (com espaço depois de Bearer).
# No cabeçalho vai o access. O refresh só vai no corpo (json=) de token/refresh/ e token/blacklist/.
# Para ler o conteúdo do token, ele tem 3 partes separadas por ponto (cabeçalho.conteúdo.assinatura). Pegue a parte do meio e use:

# import base64, json

# conteudo = access.split('.')[1]
# conteudo += '=' * (-len(conteudo) % 4)
# print(json.loads(base64.urlsafe_b64decode(conteudo)))



import requests, base64, json

URL = 'http://127.0.0.1:8000/api/v1/'



# Etapa 1
# POST api/areas/ sem token. Imprima também o cabeçalho WWW-Authenticate da resposta. (Esperado: 401)
data = requests.post(URL + 'areas/')
print(data.status_code)
print("WWW-Authenticate:", data.headers.get("WWW-Authenticate"),"\n")



# Etapa 2
# POST api/token/ com a senha errada. (Esperado: 401)
senha_errada = requests.post(URL + 'token/', json={"username": "Juan", "password": "123456"})
print(senha_errada.status_code,"\n")



# Etapa 3
# POST api/token/ com a senha certa. Guarde o access e o refresh. (Esperado: 200)
senha_certa = requests.post(URL + 'token/', json={"username": "Juan", "password": "Juan123"})
print(senha_certa.status_code,"\n")

access = senha_certa.json().get("access")
refresh = senha_certa.json().get("refresh")



# Etapa 4
# Leia o conteúdo do access em Python e imprima o user_id e quanto tempo o token vale (exp - iat, em segundos).
access_conteudo = access.split('.')[1]
access_conteudo += '=' * (-len(access_conteudo) % 4)
access_dados = json.loads(base64.urlsafe_b64decode(access_conteudo))

print("User ID:", access_dados.get("user_id"))
print("Tempo de validade (segundos):", access_dados.get("exp") - access_dados.get("iat"), "\n")



# Etapa 5
# POST api/areas/ com o cabeçalho Authorization. (Esperado: 201)
areas = requests.post(URL + 'areas/', json={"nome": "Natação"}, headers={'Authorization': 'Bearer ' + access})

print(areas.status_code, "\n")



# Etapa 6
# DELETE da área criada no item 5. (Esperado: 204)
area_id = areas.json()['id']
delete = requests.delete(URL + f'area_deletar/{area_id}/', headers={'Authorization': 'Bearer ' + access})

print(delete.status_code, "\n")



# Etapa 7
# GET api/areas/ com um token inválido (ex.: 'Bearer abc.def.ghi'). (Esperado: 401)
invalido = requests.get(URL + 'areas/', headers={'Authorization': 'Bearer abc.def.ghi'})

print(invalido.status_code, "\n")



# Etapa 8
# POST api/token/refresh/ com o refresh. Troque o access antigo pelo novo. (Esperado: 200)
renovado = requests.post(URL + 'token/refresh/', json={"refresh": refresh})

print(renovado.status_code, "\n")

access = renovado.json().get("access")
refresh = renovado.json().get("refresh", refresh)



# Etapa 9
# POST api/token/blacklist/ com o refresh (logout). (Esperado: 200)
logout = requests.post(URL + 'token/blacklist/', json={"refresh": refresh})

print(logout.status_code, "\n")



# Etapa 10
# POST api/token/refresh/ de novo com o mesmo refresh. (Esperado: 401)
refresh_de_novo = requests.post(URL + 'token/refresh/', json={"refresh": refresh})

print(refresh_de_novo.status_code, "\n")



# Etapa 11
# POST api/areas/ com o access do item 8, depois do logout. Anote o resultado.
depois_logout = requests.post(URL + 'areas/', json={"nome": "Redes"}, headers={'Authorization': 'Bearer ' + access})

print(depois_logout.status_code, "\n")

print("Resultado:", depois_logout.status_code)



# ==========================================================================

# Respostas:
# 1. No item 11, o access continuou funcionando depois do logout? Por quê? (Compare com o logout da sessão na Parte 1.)
#    O access continuou funcionando depois do logout porque o logout só invalida o refresh, não o access.


# 2. Por que no JWT não foi preciso mandar o token CSRF?
#    Porque o JWT não depende de cookies, então não há risco de CSRF.
#    O token é enviado no cabeçalho Authorization, e não em um cookie, então não há vulnerabilidade de CSRF.


# 3. O conteúdo do token é criptografado? O que impede alguém de alterar o user_id?
#    Não, o conteúdo do token não é criptografado, ele é apenas codificado em base64.
#    O que impede alguém de alterar o user_id é a assinatura do token.
#    Se alguém alterar o conteúdo do token, a assinatura não será mais válida, e o servidor rejeitará o token como inválido.

# ==========================================================================