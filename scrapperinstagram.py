import requests
import json
# Defina os cookies corretamente
cookies = (
    "ps_n=1; "
    "datr=wGURaERLiN3kuj8Vp7zGYlj3; "
    "ds_user_id=2448742298; "
    "csrftoken=E1JM3J3GU37s9MXW9D0VzRftE9VVBA4y; "
    "ig_did=89ACB30B-7EE1-4240-8322-833E48471829; "
    "ps_l=1; "
    "wd=986x872; "
    "mid=aBFlwAABAAEVMKbVZSkqZlzSY3jZ; "
    "sessionid=2448742298%3Ajsf7diDeyWepOl%3A16%3AAYfA9yxd3_GRunoA2rUrILZta1WrqjwShujSsYMedA; "
    "dpr=2; "
    "rur=NHA\\0542448742298\\0541777507348:01f778aa5b5f2f956c31a08715673a248d0f46dfb453327e0c8d2ee8b2d165db577f3cc9"
)

# Cabeçalhos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.instagram.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": cookies
}

# URL para fazer a requisição
url_fetch_username = "https://www.instagram.com/web/search/topsearch/?context=blended&query=pedro&rank_token=0.3953592318270893&count=10"
response = requests.get(url_fetch_username, headers=HEADERS)


# Aqui, substitua pelo seu JSON carregado. Exemplo:
data = response.json()

users = data['users']
# Lista com todos os usuários (sem filtro)
all_users = [
    {
        "nome": user["user"]["full_name"],
        "username": user["user"]["username"],
        "foto": user["user"]["profile_pic_url"],
        "verificado": user["user"]["is_verified"],
        "privado": user["user"]["is_private"]
    }
    for user in users
]

# Usuários verificados (com selo azul)
verified_users = [user for user in all_users if user["verificado"]]

# Usuários sem verificação
non_verified_users = [user for user in all_users if not user["verificado"]]

# Mostrar os resultados
print("=== TODOS OS USUÁRIOS ===")
for user in all_users:
    print(f'{user["nome"]} (@{user["username"]}) - Foto: {user["foto"]}')

print("\n=== USUÁRIOS VERIFICADOS ===")
for user in verified_users:
    print(f'{user["nome"]} (@{user["username"]}) - Foto: {user["foto"]}')

print("\n=== USUÁRIOS NÃO VERIFICADOS ===")
for user in non_verified_users:
    print(f'{user["nome"]} (@{user["username"]}) - Foto: {user["foto"]}')
