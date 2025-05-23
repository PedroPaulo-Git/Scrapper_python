import os
import time
import base64
import requests
import json
import random
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
from instaloader import Instaloader, Profile
from instaloader.exceptions import TwoFactorAuthRequiredException
from routes.getcode2fa import get_2fa_code
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# limiter = Limiter(key_func=get_remote_address)
load_dotenv()

# CACHE JSON FILE
cache_file = "cached_profiles.json"
if not os.path.exists(cache_file):
    with open(cache_file, "w") as f:
        json.dump({}, f)

# COOKIES PEGOS DA SESSÃO LOGADA
cookies = {
    "ps_n": "1",
    "datr": "Gk8uaNzPs1xAinX1z_se8Ugj",
    "ig_nrcb": "1",
    "ds_user_id": "2448742298",
    "csrftoken": "Qnk9X2CjRkqUG8gjTLVCY94PgHcM9vYF",
    "ig_did": "60759FC5-06AD-4A97-90B4-D1AE1D61D99D",
    "ps_l": "1",
    "wd": "1920x959",
    "mid": "aC5PGgABAAEt6893m-GnP6UOw2sG",
    "sessionid": "2448742298%3AoFCk8gO25GUD2J%3A14%3AAYfDHk0wFv-FeTg_n-euGulx98TR2RIscqFu3KpCxg",
    "dpr": "1",
    "rur": "NHA,2448742298,1779404992:01f7736e6f36f872dfedadc76bd2868398837d0cd4c61651bac3b9402c87dd55b8bc09f8"
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

# Blueprint para rota básica de infos
user_basic_infos_route = Blueprint('user_basic_infos', __name__)
highlights_route = Blueprint('highlights_route', __name__)
followers_route = Blueprint('followers_route', __name__)
user_info_cache = Blueprint('user_info_cache', __name__)

# Sessões em memória
L = None
_sessions = {}
CACHE_FOLDER = "cache"
os.makedirs(CACHE_FOLDER, exist_ok=True)

# <-- FUNÇÕES DE CACHE

def cache_get(key, ttl=21600):
    path = os.path.join(CACHE_FOLDER, f"{key}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    if time.time() - data.get("timestamp", 0) > ttl:
        return None
    return data.get("value")

def cache_set(key, value):
    path = os.path.join(CACHE_FOLDER, f"{key}.json")
    data = {"timestamp": time.time(), "value": value}
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)

_cached_profiles = None

def load_cached_profiles():
    global _cached_profiles
    if _cached_profiles is None:
        with open(cache_file, "r") as f:
            _cached_profiles = json.load(f)
    return _cached_profiles

def save_cached_profiles():
    with open(cache_file, "w") as f:
        json.dump(_cached_profiles, f, indent=4)

def login_instaloader(username, password, max_retries=3, min_time_between_reqs=60):
    global _sessions

    if username in _sessions:
        print(f"Reutilizando sessão em memória para {username}.")
        return _sessions[username]

    L = Instaloader()
    session_filename = f"session-{username}"

    try:
        if os.path.exists(session_filename):
            print("Tentando carregar a sessão do arquivo...")
            L.load_session_from_file(username, session_filename)
            print(f"Sessão carregada com sucesso para {username}.")
        else:
            print("Nenhuma sessão encontrada. Realizando login...")
            try:
                print("Tentando login sem 2FA...")
                L.login(username, password)
                print(f"Login bem-sucedido com {username} sem 2FA.")
            except TwoFactorAuthRequiredException:
                print("2FA requerido! Obtendo código...")
                for attempt in range(1, max_retries + 1):
                    print(f"Tentativa {attempt} para obter código 2FA...")
                    code = get_2fa_code()
                    if code:
                        try:
                            L.two_factor_login(code)
                            print(f"Login bem-sucedido com {username} usando 2FA.")
                            break
                        except Exception as e:
                            print(f"Erro no 2FA: {str(e)}")
                            if attempt == max_retries:
                                raise
                    else:
                        print("Código 2FA não encontrado. Tentando novamente...")
                    time.sleep(5)
            L.save_session_to_file(session_filename)
            print("Sessão salva com sucesso!")

        _sessions[username] = L
        return L

    except Exception as e:
        print(f"Erro durante o login: {str(e)}")
        raise

def fetch_users(username):
    global L

    if L is None:
        try:
            insta_user = os.getenv("INSTA_USER")
            insta_pass = os.getenv("INSTA_PASS")
            L = login_instaloader(insta_user, insta_pass)
        except Exception as e:
            return {"error": f"Login falhou: {str(e)}"}

    try:
        profile = Profile.from_username(L.context, username)
        user_info = {
            "username": profile.username,
            "full_name": profile.full_name,
            "picture": profile.profile_pic_url,
            "verificado": profile.is_verified,
            "privado": profile.is_private
        }
        return user_info
    except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "500" in error_msg or "Please wait a few minutes" in error_msg:
                print(f"⚠️ Interrompido: erro crítico detectado - {error_msg}")
                return {"error": "Serviço temporariamente indisponível. Tente novamente mais tarde."}
            return {"error": error_msg}
        
def get_instaloader_session():
    global L
    if L:
        return L
    insta_user = os.getenv("INSTA_USER")
    insta_pass = os.getenv("INSTA_PASS")
    L = login_instaloader(insta_user, insta_pass)
    return L

import mimetypes

image_cache = {}

def convert_image_to_base64(image_url):
    if image_url in image_cache:
        return image_cache[image_url]
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code != 200:
            return {"error": "Erro ao baixar a imagem"}

        content_type = response.headers.get("Content-Type")
        if not content_type:
            content_type = mimetypes.guess_type(image_url)[0] or "image/jpeg"

        image_bytes = response.content
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        data_url = f"data:{content_type};base64,{base64_image}"
        
        image_cache[image_url] = data_url
        return data_url
    except Exception as e:
        return {"error": f"Erro ao converter a imagem para base64: {str(e)}"}



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


@user_basic_infos_route.route('/userbasicinfos', methods=['GET'])
# @limiter.limit("5 per minute") 
def get_user_basic_infos():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Parâmetro 'username' é obrigatório"}), 400
    cache_key = f"basicinfo_{username}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(cached)


    user_info = fetch_users(username)
    if "error" in user_info:
        return jsonify({"error": user_info["error"]}), 500
    time.sleep(random.uniform(2, 5))
    profile_pic_url = user_info.get("picture")
    if not profile_pic_url:
        return jsonify({"error": "Imagem de perfil não encontrada"}), 404

    profile_pic_base64 = convert_image_to_base64(profile_pic_url)
    if isinstance(profile_pic_base64, dict) and "error" in profile_pic_base64:
        return jsonify({"error": profile_pic_base64["error"]}), 500

    basic_info = {
        "username": user_info["username"],
        "full_name": user_info["full_name"],
        "picture": profile_pic_base64,
        "verificado": user_info["verificado"],
        "privado": user_info["privado"]
    }
    return jsonify(basic_info)

@highlights_route.route('/userhighlights', methods=['GET'])
def get_user_highlights():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Informe o username na URL: /userhighlights?username=usuario'}), 400
    cache_key = f"highlights_{username}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify({'status': 'success', 'thumbnail_base64': cached})

    try:
        insta_user = os.getenv("INSTA_USER")
        insta_pass = os.getenv("INSTA_PASS")
        L = login_instaloader(insta_user, insta_pass)
        if not L:
            return jsonify({'error': 'Falha no login do Instaloader'}), 401
        time.sleep(random.uniform(2, 5))
        profile = Profile.from_username(L.context, username)
        user_highlights = L.get_highlights(profile)

        highlight_found = next(user_highlights, None)
        if not highlight_found:
            return jsonify({'message': 'Nenhum highlight encontrado para este usuário'}), 404

        stories = list(highlight_found.get_items())
        if not stories:
            return jsonify({'message': 'Highlight não possui histórias'}), 404

        first_story = stories[0]
        image_url = first_story.url
        base64_image = convert_image_to_base64(image_url)

        return jsonify({
            'status': 'success',
            'thumbnail_base64': base64_image,
        })

    except Exception as e:
        print(f"Erro ao buscar highlights: {e}")
        return jsonify({'error': 'Erro ao buscar highlights'}), 500
@followers_route.route('/userfollowers', methods=['GET'])
def get_user_followers():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Informe o username na URL: /userfollowers?username=usuario'}), 400
    cache_key = f"followers_{username}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify({"status": "success", "followers": cached})

    try:
        # Informações de login
        insta_user = os.getenv("INSTA_USER")
        insta_pass = os.getenv("INSTA_PASS") # Substitua pela sua senha

        # Realizando o login
        L = login_instaloader(insta_user, insta_pass)

        # Pegando o perfil do usuário
        time.sleep(random.uniform(2, 5))        
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
