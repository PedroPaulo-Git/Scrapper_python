from flask import Blueprint, jsonify, request
import requests
from utils import get_headers

user_basic_infos_route = Blueprint('user_basic_infos', __name__)

def fetch_users(username):
    headers = get_headers()
    url = f"https://www.instagram.com/web/search/topsearch/?context=blended&query={username}&rank_token=0.3953592318270893&count=10"
    response = requests.get(url, headers=headers)
    data = response.json()
    users = data.get('users', [])
    
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

@user_basic_infos_route.route('/userbasicinfos', methods=['GET'])
def get_user_basic_infos():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Parâmetro 'username' é obrigatório"}), 400
    
    all_users = fetch_users(username)
    basic_infos = [
        {
            "username": user["username"],
            "full_name": user["full_name"],
            "picture": user["picture"]
        }
        for user in all_users
    ]
    return jsonify(basic_infos)
