import os
import json
import requests
from flask import Blueprint, jsonify, request

# CACHE JSON FILE
cache_file = "cached_profiles.json"
if not os.path.exists(cache_file):
    with open(cache_file, "w") as f:
        json.dump({}, f)

# COOKIES PEGOS DA SESSÃO LOGADA
cookies = {
    "sessionid": "TUA_SESSIONID_AQUI",
    "csrftoken": "TEU_CSRF_AQUI"
    # Adiciona mais se quiser, mas isso aqui já resolve
}

# HEADERS PRA CAMUFLAR COMO SE FOSSE NAVEGADOR
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.instagram.com/",
    "X-CSRFToken": cookies["csrftoken"],
    "X-Requested-With": "XMLHttpRequest"
}

# CRIA A ROTA FLASK
user_info_cache = Blueprint('user_info_cache', __name__)

@user_info_cache.route('/cacheduserinfos', methods=['GET'])
def cached_user_info():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'username obrigatório'}), 400

    with open(cache_file, "r") as f:
        cached_data = json.load(f)

    if username in cached_data:
        return jsonify(cached_data[username])  # Já tem salvo

    url = f"https://www.instagram.com/web/search/topsearch/?context=blended&query={username}&count=1"
    response = requests.get(url, headers=HEADERS, cookies=cookies)

    if response.status_code != 200:
        return jsonify({'error': 'Erro na requisição ao Instagram'}), 500

    data = response.json()
    users = data.get("users", [])
    if not users:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    user_data = {
        "username": users[0]["user"]["username"],
        "full_name": users[0]["user"]["full_name"],
        "profile_pic": users[0]["user"]["profile_pic_url"],
        "verificado": users[0]["user"]["is_verified"],
        "privado": users[0]["user"]["is_private"]
    }

    # Salva no cache
    cached_data[username] = user_data
    with open(cache_file, "w") as f:
        json.dump(cached_data, f, indent=4)

    return jsonify(user_data)
