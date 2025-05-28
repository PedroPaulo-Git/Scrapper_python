# from flask import Flask, request, jsonify
# # from routes.userbasicinfos import user_basic_infos_route
# # from routes.followers import followers_route
# # from routes.highlight import highlights_route
# # from routes.user_cache import user_info_cache  # <- ADICIONA ISSO
# from routes.login import user_basic_infos_route, followers_route, highlights_route, user_info_cache
# from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, origins=["https://instaviewpro.vercel.app","http://localhost:3000","https://instaviewpro.site"], methods=["GET","POST","OPTIONS"])

# # Registrando a rota
# app.register_blueprint(highlights_route)
# app.register_blueprint(user_basic_infos_route)
# app.register_blueprint(followers_route)
# app.register_blueprint(user_info_cache) 


# @app.route("/proxy/userbasicinfos")
# def proxy_user_basic_infos():
#     username = request.args.get("username")
#     if not username:
#         return jsonify({"error": "username é obrigatório"}), 400

#     try:
#         response = requests.get(
#             f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
#             headers=HEADERS,
#             cookies=COOKIES,
#             timeout=10
#         )
#         return jsonify(response.json()), response.status_code
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# @app.route('/validate-purchase')
# def validate_purchase():
#     token = request.args.get("token")

#     if not token:
#         return jsonify({"valid": False})

#     try:
#         with open("purchases.txt", "r") as file:
#             compras = file.readlines()
#             for linha in compras:
#                 if token.strip() in linha.strip():
#                     return jsonify({"valid": True})
#     except FileNotFoundError:
#         pass

#     return jsonify({"valid": False})

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     try:
#         if request.is_json:
#             data = request.get_json()
#         else:
#             data = request.form.to_dict()

#         print("Compra recebida:", data)

#         token = data.get("purchase[token]") or data.get("purchase.extra_fields[token]")  # substitua com o nome real do campo no Gumroad

#         if token:
#             with open("purchases.txt", "a") as file:
#                 file.write(f"{token}\n")

#         return '', 200
#     except Exception as e:
#         print("Erro no webhook:", str(e))
#         return jsonify({"error": "Webhook error"}), 400

# if __name__ == "__main__":
#     app.run(debug=True)

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, origins=["https://instaviewpro.vercel.app", "http://localhost:3000", "https://instaviewpro.site"], methods=["GET", "POST", "OPTIONS"])

# COOKIES E HEADERS COPIADOS DA SESSÃO VÁLIDA
HEADERS = {
    "User-Agent": "Instagram 261.1.0.21.111 Android (30/11; 420dpi; 1080x2340; Xiaomi; Redmi Note 8; ginkgo; qcom; pt_BR)",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "X-IG-App-ID": "936619743392459",
    "Referer": "https://www.instagram.com/",
    "X-CSRFToken": "K2TX6JCPdm2VzoZQGVwLJ3iGcLZVjBEM",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.instagram.com",
    "Connection": "keep-alive"
}

COOKIES = {
    "ps_n": "1",
    "ig_nrcb": "1",
    "ds_user_id": "2448742298",
    "csrftoken": "K2TX6JCPdm2VzoZQGVwLJ3iGcLZVjBEM",
    "ig_did": "3C1020B6-3EF6-412F-8102-CC699EE762C4",
    "ps_l": "1",
    "wd": "1920x959",
    "mid": "aDaJDgALAAHwqXftnXK73ryfmjYi",
    "sessionid": "2448742298%3A7jqbacfu1qdRiV%3A23%3AAYfmYdGM9GS9_yhCkJERou-pecm2BATJXiL6cOZCag",
    "rur": "\"FRC\\0542448742298\\0541779940539:01f7d9539776d32207c015d70735d6f86460527579b50824ad38a01e04acf8131b7f989c\""
}

NGROK_URL = os.getenv("NGROK_URL", "https://6415-138-121-33-169.ngrok-free.app")

@app.route("/proxy/userbasicinfos")
def proxy_user_basic_infos():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "username é obrigatório"}), 400

    try:
        # ✅ Cabeçalhos que ignoram o aviso do ngrok
        headers = {
            "ngrok-skip-browser-warning": "true",  # Força ignorar a página de aviso
            "User-Agent": "Mozilla/5.0 (compatible; MyScraper/1.0)"  
        }

        response = requests.get(
            f"{NGROK_URL}/userbasicinfos",  # atenção: rota original do seu backend local
            params={"username": username},
            headers=headers,
            timeout=10
        )

        # Se a resposta for HTML (o que ainda pode ser erro), trate para debug
        if "text/html" in response.headers.get("Content-Type", ""):
            return jsonify({"error": "Recebeu HTML ao invés de JSON", "html_snippet": response.text[:300]}), 500

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=9090, debug=True)
