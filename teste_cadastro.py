# Agora é com você. Crie o arquivo teste_cadastro.py que teste a API de cadastro de usuários.
# Use dados novos (um cpf, username e email que ainda não existam no banco).
# O script deve, nesta ordem, imprimir o status_code e o JSON de cada item:


# Dicas:
# Monte os dados em um dicionário e altere só o que precisa em cada teste:

# novo = {
#     'cpf': '...',
#     'username': '...',
#     ...
# }

# O cabeçalho do token é o mesmo da aula passada: headers={'Authorization': 'Bearer ' + access}.
# No PUT, mande todos os campos do UsuarioSerializer (o PUT substitui o objeto inteiro).
# Para rodar o script várias vezes, mude o cpf, username e email antes de cada execução (ou apague o usuário pelo admin).



import requests, random

URL = 'http://127.0.0.1:8000/api/v1/'


# Dados novos a cada execução (cpf com 11 números, username e email únicos)
sufixo = random.randint(100000, 999999)
novo = {
    'cpf': f'{random.randint(0, 10**11 - 1):011d}',
    'username': f'teste{sufixo}',
    'first_name': 'Teste',
    'last_name': 'Cadastro',
    'email': f'teste{sufixo}@email.com',
    'nascimento': '2000-01-01',
    'password': 'Senha@12345',
    'password2': 'Senha@12345',
}

def mostrar(resposta):
    print(resposta.status_code)
    print(resposta.json(), "\n")



# Etapa 1
# POST api/cadastro/ com password2 diferente de password. (Esperado: 400)
dados = {**novo, 'password2': 'outra-senha'}
password_diferente = requests.post(URL + 'cadastro/', json=dados)
mostrar(password_diferente)


# Etapa 2
# POST api/cadastro/ com o CPF com letras (ex.: 1234567890a). (Esperado: 400 com a mensagem do validate_cpf)
dados = {**novo, 'cpf': '1234567890a'}
letras_CPF = requests.post(URL + 'cadastro/', json=dados)
mostrar(letras_CPF)


# Etapa 3
# POST api/cadastro/ com os dados corretos. Guarde o access e o refresh que vieram na resposta. (Esperado: 201)
dados_corretos = requests.post(URL + 'cadastro/', json=novo)
mostrar(dados_corretos)

access = dados_corretos.json().get('access')
refresh = dados_corretos.json().get('refresh')


# Etapa 4
# Confira que a resposta do item 3 não tem password nem password2. Imprima True ou False.
corpo = dados_corretos.json()
usuario = corpo.get('usuario', {})
sem_senha = not any(campo in dicionario for dicionario in (corpo, usuario)
                    for campo in ('password', 'password2'))
print(sem_senha, "\n")


# Etapa 5
# POST api/cadastro/ com os mesmos dados do item 3. (Esperado: 400)
mesmos_dados = requests.post(URL + 'cadastro/', json=novo)
mostrar(mesmos_dados)


# Etapa 6
# GET api/eu/ sem token. (Esperado: 401)
eu_semToken = requests.get(URL + 'eu/')
mostrar(eu_semToken)


# Etapa 7
# GET api/eu/ com o access do item 3. (Esperado: 200)
cabecalho = {'Authorization': 'Bearer ' + access}
eu_comAccess = requests.get(URL + 'eu/', headers=cabecalho)
mostrar(eu_comAccess)


# Etapa 8
# PUT api/eu/ mudando o first_name e mandando um cpf diferente. Imprima o first_name e o cpf da resposta. (Esperado: 200, first_name novo e cpf antigo)
dados_put = {
    'cpf': '00000000000',            # tentativa de trocar o cpf
    'username': novo['username'],
    'first_name': 'NomeNovo',
    'last_name': novo['last_name'],
    'email': novo['email'],
    'nascimento': novo['nascimento'],
}
put_firstName = requests.put(URL + 'eu/', json=dados_put, headers=cabecalho)
print(put_firstName.status_code)
print("first_name:", put_firstName.json().get('first_name'))
print("cpf:", put_firstName.json().get('cpf'), "\n")


# Etapa 9
# POST api/token/ com o username e a senha cadastrados. (Esperado: 200)
cadastrados = requests.post(URL + 'token/', json={'username': novo['username'], 'password': novo['password']})
print(cadastrados.status_code)
print(cadastrados.json(), "\n")


# Etapa 10
# POST api/token/blacklist/ com o refresh (logout). (Esperado: 200)
blacklist_refresh = requests.post(URL + 'token/blacklist/', json={'refresh': refresh})
mostrar(blacklist_refresh)




# ==========================================================================

# Respostas:
# 1. Por que o cpf não mudou no item 8?
#    Porque no UsuarioSerializer o CPF está em read_only_fields.
#    O serializer ignora esse campo na entrada, então o valor enviado no PUT é descartado e o CPF antigo continua.
#    Por isso o PUT retorna 200 e não 400.

# 2. Qual a diferença entre o UsuarioCadastroSerializer e o UsuarioSerializer? Por que usamos os dois na view cadastro?
#    O UsuarioCadastroSerializer é de entrada: recebe password e password2 (write_only), valida o cpf e a confirmação de senha,
#    e cria o usuário com create_user, que grava a senha com hash.

#    O UsuarioSerializer é de saída: mostra só os dados públicos, sem senha. Na view, o primeiro valida e cria, e o segundo formata a resposta.

# 3. Por que o usuário não precisou chamar api/token/ logo depois do cadastro?
#    Porque a view cadastro já gera os tokens com RefreshToken.for_user(usuario)
#    e os devolve na resposta, então o usuário já sai do cadastro logado.

# ==========================================================================




# ==========================================================================
# Desafios (se terminar antes, tente fazer):

# Trocar a senha:
# crie PUT api/eu/senha/ que recebe password e password2. Use um serializer com os dois campos e o mesmo validate() do cadastro.
# Na view, use request.user.set_password(...) e request.user.save().

# Pergunta: depois de trocar a senha, o access antigo continua funcionando?



# Listar usuários:
# crie GET api/usuarios/ que lista todos os usuários (com o UsuarioSerializer), mas só para superusuário.
# Se não for, devolva 403. (Dica: if not request.user.is_superuser:, igual ao usuarios_listar do site.)



# Validadores de senha do Django:
# faça a API recusar senhas fracas acrescentando validators=[validate_password] no campo
# password do UsuarioCadastroSerializer (from django.contrib.auth.password_validation import validate_password).

# Pergunta: O que acontece com senha123? Por quê? (Dica: veja o AUTH_PASSWORD_VALIDATORS no settings.py.)
# ==========================================================================