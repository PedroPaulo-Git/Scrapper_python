from flask import Flask, request, jsonify
from routes.userbasicinfos import user_basic_infos_route
from routes.followers import followers_route
from routes.highlight import highlights_route
from routes.user_cache import user_info_cache  # <- ADICIONA ISSO

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://instaviewpro.vercel.app","http://localhost:3000","https://instaviewpro.site"], methods=["GET","POST","OPTIONS"])

# Registrando a rota
app.register_blueprint(highlights_route)
app.register_blueprint(user_basic_infos_route)
app.register_blueprint(followers_route)
app.register_blueprint(user_info_cache) 

@app.route('/validate-purchase')
def validate_purchase():
    token = request.args.get("token")

    if not token:
        return jsonify({"valid": False})

    try:
        with open("purchases.txt", "r") as file:
            compras = file.readlines()
            for linha in compras:
                if token.strip() in linha.strip():
                    return jsonify({"valid": True})
    except FileNotFoundError:
        pass

    return jsonify({"valid": False})

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        print("Compra recebida:", data)

        token = data.get("custom_field_token")  # substitua com o nome real do campo no Gumroad

        if token:
            with open("purchases.txt", "a") as file:
                file.write(f"{token}\n")

        return '', 200
    except Exception as e:
        print("Erro no webhook:", str(e))
        return jsonify({"error": "Webhook error"}), 400

if __name__ == "__main__":
    app.run(debug=True)
