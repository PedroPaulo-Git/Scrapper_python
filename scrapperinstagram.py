import requests
import json
# Defina os cookies corretamente
cookies = {
    "ps_n": "1",
    "datr": "jKgRaOOHaO1AbjJoJmjqS-b6",
    "ig_nrcb": "1",
    "ds_user_id": "2448742298",
    "csrftoken": "0twLk8Y2ma30MjUph43jCNjONNlzx0TW",
    "ig_did": "E66F2999-9072-407B-8C21-973E8620D5C1",
    "ps_l": "1",
    "wd": "1920x959",
    "mid": "aC5DWgALAAG19ClEEzXuSwjc3X79",
    "sessionid": "2448742298%3Aq96TCvOIQvsBqS%3A21%3AAYeD8P0ChAqO_j_PKagZjJzDnsKiRoiUuPUZv_A7ig",
    "rur": "NHA,2448742298,1779398657:01f78492556a102df1b841ba33e5054f4d76cad58a0aaa49585305dfc62a13c92162ad83"
}

# Cabeçalhos típicos de um navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.instagram.com/",
    "X-CSRFToken": cookies["csrftoken"],
    "X-Requested-With": "XMLHttpRequest"
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
