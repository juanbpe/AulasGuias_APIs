import requests

URL = 'http://127.0.0.1:8000/api/v1/'

sessao = requests.Session()


# Etapa 1
# GET api/areas/ sem login. (Esperado: 200)
semLogin_GET = sessao.get(URL + 'areas/')

print(semLogin_GET.status_code)
print(semLogin_GET.json())


# Etapa 2
# POST api/areas/ sem login. (Esperado: 403)
semLogin_POST = sessao.post(URL + 'areas/')

print("\n")
print(semLogin_POST.status_code)
print(semLogin_POST.json())


# Etapa 3
# POST api/login/ com a senha errada. (Esperado: 401)
senha = {
    "username": "Juan",
    "password": "123456",
}

loginSenhaErrada = sessao.post(URL + 'login/', json=senha)

print("\n")
print(loginSenhaErrada.status_code)
print(loginSenhaErrada.json())


# Etapa 4
# POST api/login/ com a senha certa. Imprima também os cookies recebidos. (Esperado: 200)
senhaCerta = {
    "username": "Juan",
    "password": "123",
}

loginSenhaCerta = sessao.post(URL + 'login/', json=senhaCerta)

print("\n")
print(loginSenhaCerta.status_code)
print(loginSenhaCerta.json())

print("\nCookies recebidos:")
print(sessao.cookies.get_dict())


# Etapa 5
# POST api/areas/ logado, mas sem o cabeçalho X-CSRFToken. (Esperado: 403)
logadoAreas = sessao.post(URL + 'areas/')

print("\n")
print(logadoAreas.status_code)
print(logadoAreas.json())


# Etapa 6
# POST api/areas/ logado e com o X-CSRFToken. (Esperado: 201) \\// Ps. Acredito que era para cadastrar uma área, de acordo com o item 7
criarArea = {
    "nome": "Teste",
}

logadoToken = sessao.post(URL + 'area_cadastrar/', json=criarArea, headers={'X-CSRFToken': sessao.cookies.get('csrftoken')})

print("\n")
print(logadoToken.status_code)
print(logadoToken.json())


# Etapa 7
# DELETE da área criada no item 6. (Esperado: 204)
id_area = logadoToken.json()['id']
apagarArea = sessao.delete(URL + f'area_deletar/{id_area}/', headers={'X-CSRFToken': sessao.cookies.get('csrftoken')})

print("\n")
print(apagarArea.status_code)


# Etapa 8
# POST api/logout/. Imprima os cookies de novo. (Esperado: 204)
logout = sessao.post(URL + 'logout/', headers={'X-CSRFToken': sessao.cookies.get('csrftoken')})

print("\n")
print(logout.status_code)

print("\nCookies após logout:")
print(sessao.cookies.get_dict())

# Etapa 9
# POST api/areas/ depois do logout. (Esperado: 403)
depoisLogout = sessao.post(URL + 'areas/')

print("\n")
print(depoisLogout.status_code)
print(depoisLogout.json())



# ==========================================================================
# Respostas:
# 1. Qual cookie sumiu depois do logout?

# O cookie que sumiu depois do logout foi o "sessionid", responsável por
# identificar a sessão autenticada do usuário.



# 2. Por que o item 5 deu erro, se você já estava logado?

# O item 5 deu erro 403 porque, apesar de já estar logado, a requisição
# POST foi enviada sem o cabeçalho X-CSRFToken. A autenticação por sessão
# exige essa proteção contra CSRF em requisições que modificam dados.
# ==========================================================================