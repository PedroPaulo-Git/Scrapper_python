from flask import Blueprint, jsonify
from utils import get_headers
import requests

# Criação do Blueprint
picture_bp = Blueprint('picture', __name__)

# Definindo a rota /picture
@picture_bp.route('/')
def get_picture():
    HEADERS = get_headers()  # Chama a função que retorna os headers

    url_fetch_picture = "https://www.instagram.com/web/search/topsearch/?context=blended&query=pedro&rank_token=0.3953592318270893&count=10"
    response = requests.get(url_fetch_picture, headers=HEADERS)

    data = response.json()
    users = data['users']

    all_users = [
        {
            "nome": user["user"]["full_name"],
            "username": user["user"]["username"],
            "foto": user["user"]["profile_pic_url"]
        }
        for user in users
    ]

    return jsonify(all_users)
