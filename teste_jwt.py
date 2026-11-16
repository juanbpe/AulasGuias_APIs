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
print(senha_errada.status_code)


# Etapa 3
# POST api/token/ com a senha certa. Guarde o access e o refresh. (Esperado: 200)



# Etapa 4
# Leia o conteúdo do access em Python e imprima o user_id e quanto tempo o token vale (exp - iat, em segundos).



# Etapa 5
# POST api/areas/ com o cabeçalho Authorization. (Esperado: 201)



# Etapa 6
# DELETE da área criada no item 5. (Esperado: 204)



# Etapa 7
# GET api/areas/ com um token inválido (ex.: 'Bearer abc.def.ghi'). (Esperado: 401)



# Etapa 8
# POST api/token/refresh/ com o refresh. Troque o access antigo pelo novo. (Esperado: 200)



# Etapa 9
# POST api/token/blacklist/ com o refresh (logout). (Esperado: 200)



# Etapa 10
# POST api/token/refresh/ de novo com o mesmo refresh. (Esperado: 401)



# Etapa 11
# POST api/areas/ com o access do item 8, depois do logout. Anote o resultado.




# ==========================================================================
# Respostas:
# 1. No item 11, o access continuou funcionando depois do logout? Por quê? (Compare com o logout da sessão na Parte 1.)


# 2. Por que no JWT não foi preciso mandar o token CSRF?



# 3. O conteúdo do token é criptografado? O que impede alguém de alterar o user_id?
# ==========================================================================