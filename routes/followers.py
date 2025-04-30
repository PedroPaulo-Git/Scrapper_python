# followers.py
from flask import Blueprint, jsonify, request
from routes.login import login_instaloader  # Importando a função de login
from instaloader import Profile

followers_route = Blueprint('followers_route', __name__)

@followers_route.route('/userfollowers', methods=['GET'])
def get_user_followers():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Informe o username na URL: /userfollowers?username=usuario'}), 400

    try:
        # Informações de login
        insta_username = 'pascoacacau'  # Substitua pelo seu username
        insta_password = '9BNtRiDwOz'  # Substitua pela sua senha

        # Realizando o login
        L = login_instaloader(insta_username, insta_password)

        # Pegando o perfil do usuário
        profile = Profile.from_username(L.context, username)
        
        followers = []
        for i, follower in enumerate(profile.get_followers()):
            if i >= 6:
                break
            followers.append({
                "username": follower.username,
                "full_name": follower.full_name,
                "picture": follower.profile_pic_url
            })

        return jsonify(followers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
