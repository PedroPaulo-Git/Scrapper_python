import base64
from flask import Blueprint, jsonify, request
import instaloader
import requests
from utils import get_headers
from instaloader import Instaloader
from routes.login import login_instaloader 

user_basic_infos_route = Blueprint('user_basic_infos', __name__)

usernameLogin = 'pascoacacau'  # Substitua pelo seu username
passwordLogin = '9BNtRiDwOz'  # Substitua pela sua senha


def fetch_users(username):
    # Login com Instaloader, utilizando o sistema de login
    L = login_instaloader(usernameLogin,passwordLogin)

    try:
        # Carregar o perfil do usuário
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Obter informações básicas do perfil
        user_info = {
            "username": profile.username,
            "full_name": profile.full_name,
            "picture": profile.profile_pic_url,
            "verificado": profile.is_verified,
            "privado": profile.is_private
        }

        # Retornar as informações do usuário
        return user_info
    
    except Exception as e:
        # Caso haja algum erro (usuário não encontrado, etc.), retornar o erro
        return {"error": str(e)}
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
    
@user_basic_infos_route.route('/userbasicinfos', methods=['GET'])
def get_user_basic_infos():
    username = request.args.get('username') 
    password = ''
    if not username:
        return jsonify({"error": "Parâmetros 'username' e 'password' são obrigatórios"}), 400
    
    user_info = fetch_users(username)
    profile_pic_url = user_info.get("picture")
    # print(profile_pic_url)
    
    if not profile_pic_url:
        return jsonify({"error": "Imagem de perfil não encontrada"}), 404

    # Converte a imagem para base64
    profile_pic_base64 = convert_image_to_base64(profile_pic_url)

    if "error" in profile_pic_base64:
        return jsonify({"error": profile_pic_base64["error"]}), 500
    
    # Caso o retorno seja um erro
    if "error" in user_info:
        return jsonify({"error": user_info["error"]}), 500
    
    basic_info = {
        "username": user_info["username"],
        "full_name": user_info["full_name"],
        "picture": profile_pic_base64,
        "verificado": user_info["verificado"],
        "privado": user_info["privado"]
    }
    return jsonify(basic_info)