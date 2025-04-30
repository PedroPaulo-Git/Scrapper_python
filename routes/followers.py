import base64
from io import BytesIO
import requests
from flask import Blueprint, jsonify, request
from routes.login import login_instaloader  # Importando a função de login
from instaloader import Profile

followers_route = Blueprint('followers_route', __name__)
def convert_image_to_base64(image_url):
    try:
        # Baixar a imagem como bytes diretamente da URL
        response = requests.get(image_url)
        
        # Verifica se o pedido foi bem-sucedido
        if response.status_code != 200:
            return {"error": "Erro ao baixar a imagem"}

        # Obtém os bytes da imagem
        image_bytes = response.content

        # Converte os bytes da imagem para base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        # Opcional: adicionar o tipo de conteúdo da imagem, como JPEG, PNG, etc.
        content_type = "image/jpeg"  # Ajuste conforme o tipo de imagem se necessário
        image_data_url = f"data:{content_type};base64,{base64_image}"

        return image_data_url

    except Exception as e:
        return {"error": f"Erro ao converter a imagem para base64: {str(e)}"}
    

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
            picture_base64 = convert_image_to_base64(follower.profile_pic_url)
            followers.append({
                "username": follower.username,
                "full_name": follower.full_name,
                "profile_pic_base64": picture_base64 or "data:image/png;base64,...",  # Fallback para imagem padrão
            })

        return jsonify({"status": "success", "followers": followers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
