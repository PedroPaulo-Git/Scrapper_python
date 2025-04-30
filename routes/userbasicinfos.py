from flask import Blueprint, jsonify
import requests
from utils import get_headers

# Definindo o Blueprint para a rota
user_basic_infos_route = Blueprint('user_basic_infos', __name__)

# URL para fazer a requisição
url_fetch_username = "https://www.instagram.com/web/search/topsearch/?context=blended&query=pedro&rank_token=0.3953592318270893&count=10"

# Função para obter os dados
def fetch_users():
    headers = get_headers()
    response = requests.get(url_fetch_username, headers=headers)
    data = response.json()
    users = data['users']
    
    # Lista com todos os usuários (sem filtro)
    all_users = [
        {
            "username": user["user"]["username"],
            "full_name": user["user"]["full_name"],
            "picture": user["user"]["profile_pic_url"],
            "verificado": user["user"]["is_verified"],
            "privado": user["user"]["is_private"]
        }
        for user in users
    ]
    
    return all_users

# Rota para obter as informações básicas dos usuários
@user_basic_infos_route.route('/userbasicinfos', methods=['GET'])
def get_user_basic_infos():
    all_users = fetch_users()
    basic_infos = [
        {
            "username": user["username"],
            "full_name": user["full_name"],
            "picture": user["picture"]
        }
        for user in all_users
    ]
    return jsonify(basic_infos)
