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
        profile = instaloader.Profile.from_username(L.context,username)
        print("User Has Highlight? ",profile.has_highlight_reels)
        # print("User Has Highlight? ",profile.has_highlight_reels)
     
        if not L:
            return jsonify({'error': 'Falha no login do Instaloader'}), 401


        # Pegando os highlights do usuário
        user_highlights = L.get_highlights(profile)
        
        highlight_found = None

        for h in user_highlights:
            highlight_found = h
            break

        if not highlight_found:
            return jsonify({'message': 'Nenhum highlight encontrado para este usuário'}), 404

        stories = list(highlight_found.get_items())
        if not stories:
            return jsonify({'message': 'Highlight não possui histórias'}), 404

        first_story = stories[0]

        if isinstance(first_story, StoryItem) and first_story.is_video:
            return jsonify({'message': 'Primeiro highlight é um vídeo. Ignorando...'}), 200

        # Pegando URL da imagem do primeiro story
        image_url = first_story.url
        base64_image = convert_image_to_base64(image_url)

        return jsonify({
            'status': 'success',
            # 'highlight_title': highlight_found.title,
            # 'highlightId': highlight_found.id, 
            'thumbnail_base64': base64_image,
        })

    except Exception as e:
        print("Erro ao buscar highlights:", e)
        return jsonify({'error': str(e)}), 500
