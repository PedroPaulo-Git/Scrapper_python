import os
import time
import base64
import requests
import json
import random
import mimetypes
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
from instaloader import Instaloader, Profile
from instaloader.exceptions import TwoFactorAuthRequiredException
from routes.getcode2fa import get_2fa_code

load_dotenv()

user_basic_infos_route = Blueprint('user_basic_infos', __name__)
highlights_route = Blueprint('highlights_route', __name__)
followers_route = Blueprint('followers_route', __name__)
user_info_cache = Blueprint('user_info_cache', __name__)

CACHE_FOLDER = "cache"
os.makedirs(CACHE_FOLDER, exist_ok=True)

cache_file = "cached_profiles.json"
if not os.path.exists(cache_file):
    with open(cache_file, "w") as f:
        json.dump({}, f)

_sessions = {}
image_cache = {}
L = None

HEADERS = {
    "User-Agent": "Instagram 300.0.0.0.1 Android (28/9; 420dpi; 1080x1920; Samsung; SM-G960F; starlte; exynos9810; en_US)",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.instagram.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive"
}

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

def convert_image_to_base64(image_url):
    if image_url in image_cache:
        return image_cache[image_url]
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code != 200:
            return {"error": "Erro ao baixar a imagem"}

        content_type = response.headers.get("Content-Type") or mimetypes.guess_type(image_url)[0] or "image/jpeg"
        image_bytes = response.content
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        data_url = f"data:{content_type};base64,{base64_image}"
        image_cache[image_url] = data_url
        return data_url
    except Exception as e:
        return {"error": f"Erro ao converter a imagem para base64: {str(e)}"}

def login_instaloader(username, password, max_retries=3):
    global _sessions

    if username in _sessions:
        return _sessions[username]

    L = Instaloader()
    session_filename = f"session-{username}"

    try:
        if os.path.exists(session_filename):
            L.load_session_from_file(username, session_filename)
        else:
            try:
                L.login(username, password)
            except TwoFactorAuthRequiredException:
                for attempt in range(1, max_retries + 1):
                    code = get_2fa_code()
                    if code:
                        try:
                            L.two_factor_login(code)
                            break
                        except Exception:
                            if attempt == max_retries:
                                raise
                    time.sleep(5)
            L.save_session_to_file(session_filename)

        _sessions[username] = L
        return L

    except Exception as e:
        raise Exception(f"Erro durante o login: {str(e)}")

def get_instaloader_session():
    global L
    if L:
        return L
    insta_user = os.getenv("INSTA_USER")
    insta_pass = os.getenv("INSTA_PASS")
    L = login_instaloader(insta_user, insta_pass)
    return L

@user_basic_infos_route.route('/userbasicinfos', methods=['GET'])
def get_user_basic_infos():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Parâmetro 'username' é obrigatório"}), 400

    cache_key = f"basicinfo_{username}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(cached)

    try:
        profile = Profile.from_username(get_instaloader_session().context, username)
        profile_pic_url = profile.profile_pic_url
        profile_pic_base64 = convert_image_to_base64(profile_pic_url)
        basic_info = {
            "username": profile.username,
            "full_name": profile.full_name,
            "picture": profile_pic_base64,
            "verificado": profile.is_verified,
            "privado": profile.is_private
        }
        cache_set(cache_key, basic_info)
        return jsonify(basic_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        profile = Profile.from_username(get_instaloader_session().context, username)
        user_highlights = get_instaloader_session().get_highlights(profile)
        highlight_found = next(user_highlights, None)
        if not highlight_found:
            return jsonify({'message': 'Nenhum highlight encontrado'}), 404

        stories = list(highlight_found.get_items())
        if not stories:
            return jsonify({'message': 'Highlight não possui histórias'}), 404

        first_story = stories[0]
        image_url = first_story.url
        base64_image = convert_image_to_base64(image_url)
        cache_set(cache_key, base64_image)

        return jsonify({'status': 'success', 'thumbnail_base64': base64_image})
    except Exception as e:
        return jsonify({'error': f"Erro ao buscar highlights: {str(e)}"}), 500

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
        profile = Profile.from_username(get_instaloader_session().context, username)
        followers = []
        for i, follower in enumerate(profile.get_followers()):
            if i >= 6:
                break
            picture_base64 = convert_image_to_base64(follower.profile_pic_url)
            followers.append({
                "username": follower.username,
                "full_name": follower.full_name,
                "profile_pic_base64": picture_base64 or ""
            })

        cache_set(cache_key, followers)
        return jsonify({"status": "success", "followers": followers})
    except Exception as e:
        return jsonify({'error': f"Erro ao buscar seguidores: {str(e)}"}), 500
