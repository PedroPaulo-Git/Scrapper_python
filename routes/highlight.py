import base64
import instaloader
import requests
from flask import Blueprint, jsonify, request
from instaloader import Instaloader, StoryItem
from routes.login import login_instaloader

highlights_route = Blueprint('highlights_route', __name__)

def convert_image_to_base64(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            return None
        image_bytes = response.content
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        content_type = "image/jpeg"
        return f"data:{content_type};base64,{base64_image}"
    except Exception as e:
        print(f"Erro ao converter imagem: {str(e)}")
        return None

@highlights_route.route('/userhighlights', methods=['GET'])
def get_user_highlights():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Informe o username na URL: /userhighlights?username=usuario'}), 400

    try:
        # Dados de login do Instagram
        insta_username = 'pascoacacau'
        insta_password = '9BNtRiDwOz'
        # Login com Instaloader
        L = login_instaloader(insta_username, insta_password)
        if not L:
            return jsonify({'error': 'Falha no login do Instaloader'}), 401

        profile = instaloader.Profile.from_username(L.context, username)
        print("User Has Highlight? ", profile.has_highlight_reels)
        
        # Pegando os highlights do usuário
        user_highlights = L.get_highlights(profile)
        
        highlight_found = None
        stories = []  # Garantir que stories seja uma lista vazia por padrão

        for h in user_highlights:
            highlight_found = h
            break

        if not highlight_found:
            return jsonify({'message': 'Nenhum highlight encontrado para este usuário'}), 404

        print(highlight_found)
        print(user_highlights)
        
        # Garantir que stories tenha itens
        stories = list(highlight_found.get_items())
        if not stories:
            return jsonify({'message': 'Highlight não possui histórias'}), 404

        print(stories)
        
        # Vai retornar o primeiro item, ignorando se é vídeo ou foto
        first_story = stories[0]
        image_url = first_story.url  # Isso sempre retorna uma imagem (foto ou thumb de vídeo)
        base64_image = convert_image_to_base64(image_url)

        return jsonify({
            'status': 'success',
            'thumbnail_base64': base64_image,
        })

    except Exception as e:
        print(f"Erro ao buscar highlights: {e}")
        return jsonify({'error': 'Erro ao buscar highlights'}), 500
